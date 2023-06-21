# Instalación

```sh
pip install pygame termcolor numpy argparse pickle
```

Para ejecutar el servidor en nuestra máquina en el puerto 5555 ejecutamos, el host que tomará será el de nuestra computadora.

```sh
python server.py 5555
```

Para ejecutar el cliente lo hacemos de esta forma, podemos especificar el host, pero si no lo hacemos el programa asume que el servidor corre en la misma computadora. 

```sh
python client.py --host {IP DEL SERVIDOR} --port 5555 --username fercho
```

El puerto por defecto es el 5555 pero se puede editar en el servidor, hay que especificar un username.