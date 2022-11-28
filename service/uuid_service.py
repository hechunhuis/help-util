import uuid
from commons.color import Colors

class UUIDService:

    def getUUIDByTime(self):
        '''
        根据时间戳生成 uuid ,保证全球唯一
        '''
        Colors.print(Colors.OKCYAN, "------基于时间戳生成UUID------")
        get_timestamp_uuid = uuid.uuid1()
        Colors.print(Colors.OKGREEN, "UUID:%s"%self.filterChar(get_timestamp_uuid))
    
    def getUUIDByRan(self):
        '''
        根据 随机数生成 uuid
        既然是随机就有可能真的遇到相同的，但这就像中奖似的，几率超小，因为是随机而且使用还方便，所以使用这个的还是比较多的。
        '''
        Colors.print(Colors.OKCYAN, "------基于随机数生成UUID------")
        get_randomnumber_uuid = uuid.uuid4()
        Colors.print(Colors.OKGREEN, "UUID:%s"%self.filterChar(get_randomnumber_uuid))
    
    def getUUIDBySpec(self):
        '''
        基于名字和MD5散列值生成的uuid
        里面的namespace和具体的字符串都是我们指定的
        '''
        Colors.print(Colors.OKCYAN, "------基于MD5生成UUID------")
        name = input("请输入名称(name):")
        get_specifiedstr_uuid = uuid.uuid3(uuid.NAMESPACE_DNS, name)
        Colors.print(Colors.OKGREEN, "UUID:%s"%self.filterChar(get_specifiedstr_uuid))
    
    def getUUIDBySha(self):
        '''
        和uuid3()貌似并没有什么不同，写法一样，也是由用户来指定namespace和字符串
        不过这里用的散列并不是MD5，而是SHA1.
        '''
        Colors.print(Colors.OKCYAN, "------基于SHA生成UUID------")
        name = input("请输入名称(name):")
        get_specifiedstr_SHA1_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, name)
        Colors.print(Colors.OKGREEN, "UUID:%s"%self.filterChar(get_specifiedstr_SHA1_uuid))
    
    def filterChar(self, uuid):
        '''
        过滤字符“-”
        '''
        while True:
            choise = input("\n是否过滤字符\"-\"[Y/N]:")
            if "Y" == choise.upper():
                return ''.join(str(uuid).split('-'))
            elif "N" == choise.upper():
                return uuid
            else:
                Colors.print(Colors.FAIL, "输入选项不合法,请重新输入！")
            