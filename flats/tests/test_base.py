from flats.models import Flat


class DummyFlat():
    # Створення в базі додаткових даних, потрібних для конкретного класу тестів

    def create_dummy_flat(self, id=1, flat_No="25а", floor_No=2,
                                entrance_No=3, flat_99=25):
        # створюємо квартиру:
        flat = Flat(id=id, flat_No=flat_No, floor_No=floor_No,
                    entrance_No=entrance_No, flat_99=flat_99)
        flat.save()
        # print('created flat:', flat)
        return flat

    def create_dummy_building(self, floors=(0,1,2,), entrances=(1,2,3,)):
        for f in floors:
            for e in entrances:
                for i in range(f+e):
                    no = f*100 + e*10 + i+1
                    flat_No = str(no)
                    # створюємо квартиру:
                    flat = Flat(flat_No=flat_No, floor_No=f,
                                entrance_No=e, flat_99=no)
                    flat.save()
        # print('created building')

