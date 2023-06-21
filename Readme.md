# Instalación

```sh
pip install pygame termcolor numpy argparse pickle
```

## Ejecutar un servido

Para ejecutar el servidor en nuestra máquina en el puerto 5555 ejecutamos, el host que tomará será el de nuestra computadora. 

```sh
python server.py 5555
```

**Nota**

Los puertos admitidos son los siguientes

- 3000
- 4000
- 5555

## Ejecución del cliente

Esta vez el cliente será el que elija de entre todos los servidores que pueda escanear en esos puertos y lo añadirá a la lista de conexiones si ha encontrado algo. Lo único que hay que hacer para correr un cliente es ejecutar el siguiente comando con nuestro nombre de usuario y el balanceador de carga elejirá un servidor.

```sh
python main.py --username fercho524
```