from abc import ABC


class OrderService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_order_saga_maneger(self):
        pass

    order_repository: OrderRepository
    event_publiser: DomainEventPublisher

    def ceateOrder(self, order_details: OrderDetails) -> Order:
        # ファクトリメソットでOrderを作成
        order_and_events: ResultWithEvents = Oeder.ceate_order(...)
        order: Order = order_and_events.result

        # 永続化
        order_repository.save(order)

        event_publiser.publish(
            order.class,
            str(order.get_id()),
            order_and_events.events
        )

        data: CreateOrderSagaState = CreateOrderSagaState(
            order.get_id(),
            order_details
        )

        create_order_saga_maneger.create(
            date,
            Order.class,
            order.get_id()
        )

        return order
