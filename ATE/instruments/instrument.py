## imports ##
import pyvisa

## instrument class ##
class Instrument():
    def __init__(self, resource_id = None) -> None:
        # private vars
        self._resource_id = resource_id
        self._resource = None
        
        # public
        self.id = None

        # setup
        if self._resource_id:
            self.open()

    ## resource connection ##
    def open(self, resource_id: str = None) -> None:
        if resource_id:
            self._resource_id = resource_id

        self._resource = pyvisa.ResourceManager().open_resource(self._resource_id)
        self._resource.timeout = 5000

        id_keys = ['mfg', 'model num', 'serial num', 'version num']
        id_vals = self._qr('*IDN?').replace('\n', '').split(',')

        self.id = dict(zip(id_keys, id_vals))

    def close(self) -> None:
        if self._resource:
            self._resource.close()

    def _wr(self, dat: str = '') -> None:
        self._resource.write(dat)
    
    def _rd(self) -> list:
        return self._resource.read()
    
    def _qr(self, dat: str = ''):
        return self._resource.query(dat)

## demo ##
# list all connected instruments

if __name__ == '__main__':
    # get resources
    rm = pyvisa.ResourceManager()
    resources = rm.list_resources()

    # filter out com ports
    resources = [res for res in resources if len(res.split('::')) > 2]

    print(f'connected resources: {resources}')

    for res in resources:
        inst = Instrument(res)
        print(inst.id)
