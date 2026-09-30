#!/bin/bash
# Shared by native Installer scripts. No commands are accepted from app clients.
set -euo pipefail
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LC_ALL=C
LABEL=com.alwaysawake.mac.installed.helper
HELPER=/Library/PrivilegedHelperTools/com.alwaysawake.mac.installed.helper
PLIST=/Library/LaunchDaemons/com.alwaysawake.mac.installed.helper.plist
PIN='/Library/Application Support/pika/installed-client.requirement'
JOURNAL='/Library/Application Support/Always Awake/recovery.json'
APP=/Applications/pika.app
fail() { echo "pika Installer: $*" >&2; exit 1; }
[[ "$(id -u)" == 0 ]] || fail 'Run this package with the macOS Installer administrator prompt.'
# Installing to an offline volume cannot safely manage this Mac's launchd job.
[[ "${3:-/}" == / ]] || fail 'Only installation on the current startup disk is supported.'
secure_directory() {
    local path="$1" mode
    [[ ! -L "$path" ]] || fail "Refusing symbolic-link directory: $path"
    [[ ! -e "$path" ]] && return
    [[ -d "$path" && "$(stat -f %u "$path")" == 0 ]] || fail "Directory must be owned by root: $path"
    mode="$(stat -f %Lp "$path")"
    (( (8#$mode & 022) == 0 )) || fail "Directory must not be writable by group or others: $path"
}
secure_file() {
    local path="$1" mode
    [[ ! -L "$path" ]] || fail "Refusing symbolic-link file: $path"
    [[ ! -e "$path" ]] && return
    [[ -f "$path" && "$(stat -f %u "$path")" == 0 ]] || fail "File must be a root-owned regular file: $path"
    mode="$(stat -f %Lp "$path")"
    (( (8#$mode & 022) == 0 )) || fail "File must not be writable by group or others: $path"
}
validate_paths() {
    local path
    for path in /Library /Library/LaunchDaemons /Library/PrivilegedHelperTools '/Library/Application Support' '/Library/Application Support/pika' '/Library/Application Support/Always Awake'; do
        secure_directory "$path"
    done
    for path in "$HELPER" "$PLIST" "$PIN" "$JOURNAL"; do secure_file "$path"; done
    [[ -d /Applications && ! -L /Applications && "$(stat -f %u /Applications)" == 0 ]] || fail 'Invalid /Applications directory.'
    [[ ! -L "$APP" ]] || fail 'Refusing symbolic-link app installation.'
    [[ ! -e "$APP" || -d "$APP" ]] || fail 'App destination is not a directory.'
}
sleep_enabled() {
    local value
    value="$(/usr/bin/pmset -g | /usr/bin/awk '$1 == "SleepDisabled" && NF == 2 {print $2}')"
    [[ "$value" == 0 ]]
}
require_sleep_enabled() {
    sleep_enabled || fail 'Turn Session OFF in pika before installing or removing its helper. The installer will not override system power settings.'
}
require_app_closed() {
    local status=0
    /usr/bin/pgrep -x AlwaysAwake >/dev/null || status=$?
    case "$status" in
        0) fail 'pika 메뉴 → 종료 후 다시 설치하세요. 창의 ×는 종료가 아닙니다. Quit pika from its menu, then run the installer again.' ;;
        1) return 0 ;;
        *) fail 'Could not inspect running apps. Installation stopped without replacing files.' ;;
    esac
}
stop_installed_helper() {
    local job pid='' attempt
    if job="$(/bin/launchctl print "system/$LABEL" 2>/dev/null)"; then
        pid="$(echo "$job" | /usr/bin/awk '$1 == "pid" && $2 == "=" {print $3; exit}')"
        # bootout sends SIGTERM; helper's shutdown handler restores its journal.
        /bin/launchctl bootout "system/$LABEL" || fail 'Could not unload the existing pika helper. No files were removed.'
        if [[ "$pid" =~ ^[0-9]+$ ]]; then
            for attempt in {1..20}; do
                /bin/kill -0 "$pid" 2>/dev/null || break
                /bin/sleep 0.25
            done
            ! /bin/kill -0 "$pid" 2>/dev/null || fail 'Helper shutdown is still pending. No files were removed.'
        fi
    fi
    ! /bin/launchctl print "system/$LABEL" >/dev/null 2>&1 || fail 'Helper is still loaded.'
    require_sleep_enabled
    [[ ! -e "$JOURNAL" && ! -L "$JOURNAL" ]] || fail 'A power recovery record remains. Open pika and restore the session before continuing. No recovery data was deleted.'
}
