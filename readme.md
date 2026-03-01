# LANMO

LANMO VM ASM implementation 

### Run 
```console
python main.py
```

### bytecode format
```
LANMO BC:
  MAGIC          = 4B
  MAJOR_VERSION  = 2B
  MINOR_VERSION  = 2B
  CONSTANT_COUNT = 2B
  CONSTANT_TABLE = ..
  FUNCTION_COUNT = 2B 
  FUNCTION_TABLE = ..
  
CONSTANT:
  TYPE = 1B
  SIZE = 1B
  DATA = INT<4B>, STRING<XB>, FLOAT<8B>, ID<XB>

FUNCTION:
  NAME_INDEX  = 2B
  ARGS_COUNT  = 1B
  LOCAL_COUNT = 1B
  STACK_SIZE  = 2B
  CODE_COUNT  = 4B
  CODE_BODY   = XB
```