## What is asyncuo?
asyncuo is a basic and low resource usage Ultima online proxy that allows you to hide your real ip. Run asyncuo on 10 different servers and you will get 10 different IP(s). asyncuo will run a server waiting for connections and it will forward them to your shard of choice.

## How to run
asyncuo is written in plain python and it does not require any additional library to run. The main logic is based asyncio python standard module so it is recommended to use python >= 3.6.

Once you have your pyhon environment, you can run asyncuo from the command line.

    asyncuo [-h] [-li LISTEN_IP] -lp LISTEN_PORT -si SHARD_IP -sp SHARD_PORT [-ll LOG_LEVEL] -cv CLIENT_VERSION
        -li the IP the proxy should listen on
        -lp the PORT the proxy should listen on
        -si the SHARD IP to which asyncuo will connect
        -sp the SHARD PORT to which asyncuo will connect
        -cv the client version that asyncuo should use. Be sure to provide the correct one as this is affecting the protocol

## Credits
Most of the work is heavily inspired by make [uoproxy](https://github.com/MaxKellermann/uoproxy) and [GemUo](https://github.com/MaxKellermann/GemUO) work. I also went trough many open source UO project to get insipration on how to manage encryption/compression.