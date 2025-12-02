# UnixBench plugin for linux-benchmark-lib

Plugin standalone per eseguire [UnixBench 5.1.3](https://github.com/kdlucas/byte-unixbench) su linux-benchmark-lib, compilato da sorgente (il pacchetto apt è obsoleto/non funzionante su Ubuntu).

## Requisiti
- Python 3.12+
- `linux-benchmark-lib>=0.10.0`
- Tool di build: `build-essential`, `libx11-dev`, `libgl1-mesa-dev`, `libxext-dev`, `wget`

## Installazione plugin
```bash
uv pip install -e .
lb plugin install .
```
Assicurati che UnixBench sia compilato in `/opt/UnixBench` o aggiorna `workdir` nel config del plugin.

## Build UnixBench da sorgente (host o Docker)
```bash
sudo apt-get update
sudo apt-get install -y build-essential libx11-dev libgl1-mesa-dev libxext-dev wget
wget -O unixbench.tgz https://github.com/kdlucas/byte-unixbench/archive/refs/tags/v5.1.3.tar.gz
tar xvfz unixbench.tgz
sudo mv byte-unixbench-5.1.3 /opt/UnixBench
cd /opt/UnixBench && ./Run
```
Oppure costruisci l’immagine Docker del plugin:
```bash
docker build -t lb-unixbench -f lb_unixbench_plugin/Dockerfile .
docker run --rm lb-unixbench ./Run --help
```

## Configurazione
`UnixBenchConfig` campi principali:
- `threads`: concorrenza (`-c`) – default 1
- `iterations`: iterazioni (`-i`) – default 1
- `tests`: elenco test (vuoto = default suite)
- `workdir`: path che contiene `Run` (default `/opt/UnixBench`)
- `extra_args`: argomenti aggiuntivi per `Run`
- `debug`: aggiunge `--verbose`

Presets intensità:
- **low**: 1 thread, 1 iterazione
- **medium**: ~½ CPU (min 2), 1 iterazione
- **high**: CPU count (min 2), 2 iterazioni

## Uso con lb
```bash
lb plugin list --enable unixbench
lb run --no-remote --run-id ub-demo --tests unixbench
```

## Dev & test
```bash
uv venv
source .venv/bin/activate
uv pip install -e .[dev]
pytest
```

## Note su Ansible
`lb_unixbench_plugin/ansible/setup.yml` compila UnixBench da sorgente su host remoti (richiede sudo e tool di build). Nessun teardown dedicato: per rimuovere, basta cancellare `/opt/UnixBench`.
