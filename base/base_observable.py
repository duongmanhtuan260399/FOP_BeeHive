from observer import Observer


class BaseObservable:
    def __init__(self):
        self.observers = []

    def attach(self, observer: Observer) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        try:
            self.observers.remove(observer)
        except ValueError:
            pass

    def notify(self) -> None:
        for observer in self.observers:
            observer.update(self)