from alipay import AliPay
from decouple import config


class Payment:
    """支付宝支付相关操作封装"""

    @classmethod
    def get_alipay_client(cls):
        """
        初始化支付宝 SDK 客户端
        """
        app_private_key = config("APP_PRIVATE_KEY")
        alipay_public_key = config("ALIPAY_PUBLIC_KEY")
        try:
            alipay = AliPay(
                appid="2021000142698007",  # 替换为沙箱中的 app_id
                app_notify_url="http://10.7.178.30:8000/users/pay-callback/",  # 异步通知回调地址
                app_private_key_string=open(app_private_key).read(),
                alipay_public_key_string=open(alipay_public_key).read(),
                sign_type="RSA2",  # 使用 RSA2 签名算法
                debug=True,  # 沙箱环境
            )
            return alipay
        except Exception as e:
            print(f"初始化支付宝 SDK 失败: {e}")
            raise

    @classmethod
    def create_recharge_order(cls, amount, order_id):
        """
        创建支付订单 URL
        :param amount: 支付金额（元）
        :param order_id: 商户订单号
        :return: 支付页面的跳转 URL
        """
        try:
            alipay = cls.get_alipay_client()
            # 调用支付宝的接口生成支付订单
            order_string = alipay.api_alipay_trade_page_pay(
                subject="Payment Test",  # 支付商品描述
                out_trade_no=order_id,  # 商户订单号
                total_amount=amount,  # 支付金额
                return_url="http://localhost:8000/payment-success",  # 支付成功同步跳转地址TODO:前端的url
                notify_url="http://10.7.178.30:8000/users/pay-callback/",  # 异步回调地址
            )
            return "https://openapi-sandbox.dl.alipaydev.com/gateway.do?" + order_string
        except Exception as e:
            print(f"创建支付订单失败: {e}")
            raise

    @classmethod
    def handle_alipay_callback(cls, data):
        """
        处理支付宝回调通知
        :param data: 回调请求的 POST 数据
        :return: 验证是否成功
        """
        try:
            alipay = cls.get_alipay_client()
            # 验证支付宝的签名
            is_valid = alipay.verify(data, data.get("sign"))
            if is_valid:
                # 签名验证通过，处理订单状态
                print("支付宝回调验证通过，处理订单逻辑")
                # TODO: 更新数据库中订单状态，确保幂等性
                return True
            else:
                print("支付宝回调验证失败")
                return False
        except Exception as e:
            print(f"处理支付宝回调失败: {e}")
            return False
