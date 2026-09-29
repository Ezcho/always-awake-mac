#!/usr/bin/env python3
"""Explicit live integration check. Starts then stops Session only with --session.
Never changes Monitor; refuses to alter an existing or recovering session.
"""
import argparse, json, os, pathlib, select, socket, subprocess, time
parser=argparse.ArgumentParser()
parser.add_argument('--session',action='store_true')
args=parser.parse_args()
command='/Applications/pika.app/Contents/MacOS/pika-mcp'
p=subprocess.Popen([command],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
seq=0
def request(method,params={}):
 global seq
 seq+=1
 p.stdin.write(json.dumps({'jsonrpc':'2.0','id':seq,'method':method,'params':params})+'\n');p.stdin.flush()
 if not select.select([p.stdout],[],[],25)[0]:raise RuntimeError('MCP response timeout')
 reply=json.loads(p.stdout.readline())
 assert reply['id']==seq,reply
 if 'error' in reply:raise RuntimeError(reply['error'])
 return reply['result']
def call(name,arguments={}):return request('tools/call',{'name':name,'arguments':arguments})
try:
 request('initialize',{'protocolVersion':'2025-11-25','capabilities':{},'clientInfo':{'name':'pika-live-test','version':'1'}})
 p.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n');p.stdin.flush()
 assert len(request('tools/list')['tools'])==3
 print('PASS MCP initialization and tool discovery')
 result=call('pika_status');status=result['structuredContent']
 assert not result['isError'],result
 print('STATUS',json.dumps(status,ensure_ascii=False))
 endpoint=f'/tmp/pika-control-{os.getuid()}/control.sock'
 assert pathlib.Path(endpoint).stat().st_mode & 0o777==0o600
 assert pathlib.Path(endpoint).parent.stat().st_mode & 0o777==0o700
 idle=socket.socket(socket.AF_UNIX);idle.connect(endpoint)
 before=time.monotonic();result=call('pika_status');elapsed=time.monotonic()-before
 idle.close()
 assert not result['isError'] and elapsed<2,(elapsed,result)
 print('PASS idle socket does not block status; private endpoint permissions')
 if status['sessionOn'] or status['recoveryRequired'] or status['busy']:
  print('SKIP mutation checks: existing session/recovery/busy left unchanged')
 else:
  rejected=call('pika_set_monitor',{'enabled':True})
  assert rejected['isError'] and rejected['structuredContent']['code']=='session_off',rejected
  off=call('pika_set_session',{'enabled':False})
  assert not off['isError'] and not off['structuredContent']['monitorOn'],off
  print('PASS inactive Monitor rejected and Session OFF is idempotent')
  if args.session:
   started=call('pika_set_session',{'enabled':True})
   print('SESSION_START',json.dumps(started,ensure_ascii=False))
   if started['structuredContent'].get('sessionOn') or started['structuredContent'].get('recoveryRequired'):
    stopped=call('pika_set_session',{'enabled':False})
    print('SESSION_STOP',json.dumps(stopped,ensure_ascii=False))
    assert not stopped['isError'] and not stopped['structuredContent']['sessionOn'],stopped
   if started['isError']:print('BLOCKED: Session ON requires working signed/approved helper; not a passed ON test')
   else:print('PASS real Session ON/OFF via MCP')
finally:
 p.stdin.close()
 try:p.wait(timeout=5)
 except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=5)
 stderr=p.stderr.read()
 if stderr:print('STDERR',stderr)
