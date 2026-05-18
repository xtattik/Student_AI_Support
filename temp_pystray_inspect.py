import inspect
from pystray import Icon
print([m for m in dir(Icon) if 'run' in m.lower() or 'detach' in m.lower()])
print('run', inspect.signature(Icon.run))
print('run_detached', inspect.signature(Icon.run_detached))
