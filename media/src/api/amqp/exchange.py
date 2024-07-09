from faststream.rabbit import RabbitExchange

MEME_EXCHANGE = RabbitExchange("MEME", auto_delete=True)
MEDIA_EXCHANGE = RabbitExchange("MEDIA", auto_delete=True)