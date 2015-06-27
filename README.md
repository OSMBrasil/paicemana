O `paicemana` é o programa de linha de comando que viabiliza semanalmente o fluxo de trabalho para a realização colaborativa e rastreável das traduções no projeto [OSMBrasil/semanario].

- [x] Baixa semanários de [weeklyosm.eu] convertendo em markdown
- [ ] Distribui as seções do documento entre os tradutores
- [ ] Cria automaticamente toda a infraestrutura do _milestone_ semanal

## Instalação

```bash
$ git clone https://github.com/OSMBrasil/paicemana.git
$ cd paicemana
$ sudo python setup.py install
```

## Uso

```bash
$ paicemana -h
```

## Remoção

```bash
$ sudo pip uninstall paicemana
```

## Licença

[GPLv3]

[OSMBrasil/semanario]: http://www.github.com/OSMBrasil/semanario
[weeklyosm.eu]: http://weeklyosm.eu
[GPLv3]: LICENSE