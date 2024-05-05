# pyAquatemp


A simple Python 3 library for interacting with the Aquatemp API. There are different versions of the API with different endpoints and syntax. This library is intended for AquaTemp accounts that have been created with recent versions of the app. A bash implementation for older versions can be found [here](https://github.com/dst6se/aquatemp)


## Usage
The library is used by instantiating a connection object by passing the aquatemp email address and password associated with your account. 

```python
import aquatemp

dev = aquatempConnect(username, password)
dev.setTemperature(28)
dev.setPower(1)
dev.setSilent(1)
print(dev.getStatus())


```

