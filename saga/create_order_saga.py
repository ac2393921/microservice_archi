class CreateOrderSaga(SimpleSaga):
    def __init__():
        pass

    saga_definition: SagaDefinition

    def create_order_saga(
        order_service: OrderServiceProxy,
        consumer_service: ConsumerServiceProxy,
        kitchen_service: KitchenServiceProxy,
        accounting_service: AccountingServiceProxy
    ):
        saga_definition = step().with_compensation(
            order_service.reject,
            CreateOrderSagaState.make_reject_order_command
        )
        .step()
        .invoke_participant(
            consumer_service.validate_order,
            CreateOrderSagaState.make_validate_order_by_consumer_command
        )
        .step()
        .invoke_participant(
            kitchen_service.create,
            CreateOrderSagaState.make_create_ticket_command
        )
        .on_reply(
            CreateTicketReply.class,
            CreateOrderSagaState.handle_create_ticket_reply
        )
        .with_compensation(
            kitchen_service.cancel,
            CreateOrderSagaState.make_cancel_create_ticket_command
        )
        .step()
        .invoke_participant(
            accounting_service.authorize,
            CreateOrderSagaState.make_authorize_command
        )
        .step()
        .invoke_participant(
            kitchen_service.confirm_create,
            CreateOrderSagaState.make_confirm_create_ticket_command
        )
        .step()
        .invoke_participant(
            order_service.approve,
            CreateOrderSagaState.make_approve_order_command
        )
        .build()

    def get_sage_definition() -> SagaDefinition:
        return saga_definition
