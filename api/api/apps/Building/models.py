from django.db import models


# Create your models here.
class Building(models.Model):
    """
    小区楼栋模型
    """
    stated_choice = (
        (0, '未开盘'),
        (1, '已开盘'),
    )
    name = models.CharField(max_length=16, verbose_name="楼栋名称")
    house_num = models.CharField(max_length=4, verbose_name="楼栋住房数")
    stated = models.SmallIntegerField(choices=stated_choice, verbose_name="楼栋开盘状态")

    class Meta:
        db_table = "village_building"
        verbose_name = "小区楼栋"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.name


class House(models.Model):
    """
    住房模型
    """
    stated_choice = (
        (0, '未售出'),
        (1, '已售出'),
    )
    house_id = models.CharField(max_length=8, verbose_name="房号")
    house_type = models.CharField(max_length=16, verbose_name="住房户型")
    area = models.IntegerField(default=0, verbose_name="占地面积(m²)")
    sale = models.CharField(max_length=16, verbose_name="售价(元/m²)")
    stated = models.SmallIntegerField(choices=stated_choice, verbose_name="住房售出状态")
    household = models.CharField(max_length=128, null=True, verbose_name="户主id")
    uni = models.CharField(max_length=16, verbose_name="住房所在单元")
    building = models.CharField(max_length=16, verbose_name="住房所在楼栋")

    class Meta:
        db_table = "village_house"
        verbose_name = "楼栋列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % self.house_id
