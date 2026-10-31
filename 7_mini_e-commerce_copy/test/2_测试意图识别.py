from langchain_community.chat_models import ChatTongyi
from langchain_openai import ChatOpenAI

from intent_recognize.intent_recognizer_with_structured_output import INTENT_RECOGNIZER
from intent_recognize.intent_recognizer import IntentRecognizer
# llm = ChatTongyi(model="qwen-flash")
#
# recognizer = IntentRecognizer(llm)
#
# result = recognizer.recognize("我的订单号是06715421bjfab412")
# print(type(result))
# result = recognizer.recognize("我的订单号是06715421bjfab412", "human:我想退货。\nai:请你提供你的订单号。")
# print(result)
# result = recognizer.recognize("把我的地址改为北京海淀")
# print(result)
# result = recognizer.recognize("我的订单号是06715421bjfab412，我想查询我的订单，如果没发货就把地址改为北京海淀")
# print(result)
# result = recognizer.recognize("我想你了，AI宝贝")
# print(result)

llm = ChatOpenAI(
    model='qwen3.8-27b',
    base_url='https://llm-59ddchtzu57pyk9x.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
)

IntentRecognizer = IntentRecognizer(llm=llm)

result = IntentRecognizer.recognize(user_input='你好，我要退11111订单号的货物')

print(result)