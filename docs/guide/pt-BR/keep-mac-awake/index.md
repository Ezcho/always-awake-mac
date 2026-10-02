Source: https://no-sleep-pika.online/guide/pt-BR/keep-mac-awake/
Language: pt-BR

MAC GUIDE · 2026-10-02

# Como manter o Mac acordado: modo clamshell, caffeinate e pika

Compare alimentação e tampa fechada, comandos do Terminal e pika. Veja condições, limitações, bloqueio de tela e como finalizar cada método.

## Escolha conforme a tarefa

Tela apagada, bloqueio e repouso do sistema são estados diferentes. Um Mac bloqueado pode continuar trabalhando. Para monitor externo, considere clamshell; para uma tarefa temporária com a tampa aberta, caffeinate; para trabalhar fechado sem monitor externo, pika com seu serviço auxiliar.

## 1. Alimentação e modo clamshell

Com a tampa aberta, conecte energia, monitor compatível, teclado e mouse e teste antes de fechar. Uma tela que fornece energia pode substituir o carregador conforme suas especificações. Só conectar o carregador não basta. A quantidade de monitores e a resolução dependem do modelo; autorize acessórios com a tampa aberta.

[Apple · External displays](https://support.apple.com/en-us/102501)

## Ajustes com a tampa aberta

No notebook ligado à energia, procure em Ajustes do Sistema → Bateria → Opções a prevenção de repouso automático com a tela apagada. Nomes e localização variam por sistema e modelo. Preserve a senha de bloqueio. Esse ajuste não garante impedir o repouso provocado ao fechar a tampa. Anote o valor anterior.

[Apple · Sleep and wake settings](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

## 2. Usar caffeinate temporariamente

Abra o Terminal e execute abaixo. caffeinate já vem no macOS, sem sudo. Impede repouso por inatividade, mas permite apagar a tela. Deixe o processo ativo e use Control+C nesse Terminal para terminar. Não exibir mensagens é normal. A solicitação é liberada quando o processo acaba; não é um ajuste permanente.

```
caffeinate -i
```

## Tempo, tela e comandos

O primeiro exemplo dura 3.600 segundos, uma hora; o segundo também mantém a tela por 1.800 segundos, meia hora. Omita -d se não precisar da tela. O terceiro executa make de verdade até sua conclusão; use somente no projeto que pretende compilar. Um iniciador que sai imediatamente pode terminar antes da tarefa em segundo plano. Ao executar um programa, -t não é usado.

```
caffeinate -i -t 3600
```

```
caffeinate -di -t 1800
```

```
caffeinate -i make
```

## E com a tampa fechada?

-i corresponde ao repouso ocioso do sistema, -d ao da tela. Fechar a tampa é outra condição e não há garantia de funcionamento fechado sem monitor. -s só vale com energia da tomada. -u informa atividade e pode acender a tela. Escolha opções pelo efeito documentado.

## 3. Instalar pika

pika funciona no macOS 13 ou posterior, Apple Silicon e Intel. O PKG oficial completo instala app e serviço auxiliar administrador. Faça a autenticação e as aprovações do macOS pessoalmente. Abra /Applications/pika.app, confirme o serviço, ligue Session, escolha Monitor OFF se necessário e feche a tampa. A prevenção é preparada antes; a política de tela entra após fechar. Com a tampa aberta, Monitor só salva a preferência. Session OFF restaura o ajuste sem apagar imediatamente a tela. Fechar a janela não encerra o app.

[Baixar pika · 1.0.13](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)

[Ajuda de instalação](https://no-sleep-pika.online/install/)

## Verificar e encerrar

Teste uma tarefa curta, registre a hora e confira os registros e o progresso depois. É um procedimento sugerido, não comprovação de todos os modelos. pmset -g assertions apenas consulta solicitações e não comprova continuidade da rede ou com a tampa fechada. man caffeinate mostra o manual local.

```
pmset -g assertions
```

```
man caffeinate
```

## Bloqueio, rede e calor

Bloqueio não significa necessariamente repouso. Wi-Fi, VPN, limites de API, aprovações e falhas de apps podem interromper tarefas; pika não continua conversas nem reconecta a rede. Use uma superfície firme e ventilada, nunca uma bolsa. Proteção térmica, bateria ou falha do serviço podem finalizar a sessão; não há garantia contra todo superaquecimento ou descarga.

## Fontes e escopo

Comparação escrita pelo criador de no-sleep-pika, incluindo seu próprio app. Baseada em Apple, manual macOS caffeinate(8) e documentação e implementação de pika 1.0.13. Não implica endosso da Apple ou de fornecedores de IA. Mantenha a sessão apenas pelo tempo necessário.

- [Apple: If your external display is dark or low resolution](https://support.apple.com/en-us/102501)

- [Apple: Set sleep and wake settings for your Mac](https://support.apple.com/guide/mac-help/mchle41a6ccd/mac)

- [Apple: Allow USB and other accessories](https://support.apple.com/en-us/102282)

- `man caffeinate` · macOS System Manager’s Manual

Escrito pelo criador de no-sleep-pika; inclui nosso app.

[Baixar pika](https://github.com/Ezcho/always-awake-mac/releases/download/v1.0.13/pika-1.0.13.pkg)[Guia do MacBook fechado →](https://no-sleep-pika.online/guide/pt-BR/macbook-lid-closed/)[Markdown](https://no-sleep-pika.online/guide/pt-BR/keep-mac-awake/index.md)
