from django.db import models
from django.db import models
from pytils.translit import slugify
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    companyName = models.CharField("Название компании", max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def __str__(self):
        return self.companyName

    def save(self, *args, **kwargs):
        self.slug = slugify(self.companyName)
        super().save(*args, **kwargs)


class BalanceSheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания", default="")
    # Текущие активы
    activeName = models.CharField("Название актива", max_length=255, null=True, blank=True, default="Актив 1")
    year = models.IntegerField("Год", null=True, blank=True)
    cash = models.FloatField("Наличные средства", null=True, blank=True)
    accountsReceivable = models.FloatField("Дебиторская задолженность", null=True, blank=True, default=0)
    inventory = models.FloatField("Инвентаризация", null=True, blank=True, default=0)
    prepaidExpenses = models.FloatField("Предоплаченные расходы",  null=True, blank=True, default=0)
    shortTermInvestments = models.FloatField("Краткосрочные инвестиции",  null=True, blank=True, default=0)
    # Основные (долгосрочные) активы
    longTermInvestments = models.FloatField("Долгосрочные инвестиции",  null=True, blank=True, default=0)
    propertyPlantEquipement = models.FloatField("Основные средства",  null=True, blank=True, default=0)
    lessAccumulatedDepreciation = models.FloatField("За вычетом накопленной амортизации",  null=True, blank=True, default=0)
    intangibleAssets = models.FloatField("Нематериальные активы",  null=True, blank=True, default=0)
    # Общие активы
    deferredIncomeTax = models.FloatField("Отложенный налог на прибыль",  null=True, blank=True, default=0)
    other = models.FloatField("Разное (Активы)",  null=True, blank=True, default=0)
    # ------------------------------------------------------------------------------------------------
    # Текущие обязательства
    accountsPayable = models.FloatField("Кредиторская задолженность", null=True, blank=True)
    shortTermLoans = models.FloatField("Краткосрочные кредиты", null=True, blank=True)
    incomeTaxes = models.FloatField("Подлежащий уплате подоходный налог", null=True, blank=True)
    accruedSalaries = models.FloatField("Начисленная заработная плата", null=True, blank=True)
    unearnedRevenue = models.FloatField("Незаработанный доход", null=True, blank=True)
    currentPortion = models.FloatField("Текущая часть долгосрочного долга", null=True, blank=True)
    # Долгосрочные обязательства
    longTermDebt = models.FloatField("Долгосрочный долг", null=True, blank=True)
    defferedIncomeTax = models.FloatField("Отложенный налог на прибыль", null=True, blank=True)
    otherLongTerm = models.FloatField("Разное (Долгосрочные обязательства)", null=True, blank=True)
    # Собственный капитал владельца
    ownerInvestment = models.FloatField("Инвестиции владельца", null=True, blank=True)
    retainedEarnings = models.FloatField("Нераспределенная прибыль", null=True, blank=True)
    otherOwnerInvestment = models.FloatField("Разное (Собственный капитал владельца)", null=True, blank=True)

    def __str__(self):
        return f"{self.company.companyName} - {self.year} - Данные"

    # Итого оборотные активы
    def getTotalCurrentAssets(self):
        totalCurrentAssets = self.cash + self.accountsReceivable + self.inventory + self.prepaidExpenses + self.shortTermInvestments
        return totalCurrentAssets

    # Всего основных средств
    def getTotalLongTermAssets(self):
        totalLongTermAssets = self.longTermInvestments + self.propertyPlantEquipement + self.lessAccumulatedDepreciation + self.intangibleAssets
        return totalLongTermAssets

    # Итого Прочие активы
    def getTotalOtherAssets(self):
        totalOtherAssets = self.deferredIncomeTax + self.other
        return totalOtherAssets

    # Общие активы
    def getTotalAssets(self):
        totalAssets = self.getTotalCurrentAssets() + self.getTotalLongTermAssets() + self.getTotalOtherAssets()
        return totalAssets
    # ------------------------------------------------------------------------------------------------------------
    # Итого текущие обязательства
    def getTotalCurrentLiabilities(self):
        totalCurrentLiabilities = self.accountsPayable + self.shortTermLoans
        return totalCurrentLiabilities

    # Итого долгосрочные обязательства
    def getTotalLongTermLiabilities(self):
        totalLongTermLiabilities = self.longTermDebt + self.defferedIncomeTax + self.otherLongTerm
        return totalLongTermLiabilities

    # Общий собственный капитал владельца
    def getTotalOwnerEquaity(self):
        totalOwnerEquaity = self.ownerInvestment + self.retainedEarnings + self.otherOwnerInvestment
        return totalOwnerEquaity

    # Совокупные обязательства и собственный капитал владельца
    def getTotalLiabilitiesAndOwnerEquity(self):
        totalLiabilitiesAndOwnerEquity = self.getTotalCurrentLiabilities() + self.getTotalLongTermLiabilities() + self.getTotalOwnerEquaity()
        return totalLiabilitiesAndOwnerEquity
    # ------------------------------------------------------------------------------------------------------------
    # Соотношение долга (Совокупные обязательства / совокупные активы)
    def getDebtRatio(self):
        debtRatio = (self.getTotalCurrentLiabilities() + self.getTotalLongTermLiabilities()) / self.getTotalAssets()
        return debtRatio

    # Коэффициент текущей ликвидности (Текущие активы / Текущие обязательства)
    def getCurrentRatio(self):
        currentRatio = self.getTotalCurrentAssets() / self.getTotalCurrentLiabilities()
        return currentRatio

    # Оборотный капитал (Текущие активы - Текущие обязательства)
    def getWorkingCapital(self):
        workingCapital = self.getTotalCurrentAssets() - self.getTotalCurrentLiabilities()
        return workingCapital

    # Отношение активов к собственному капиталу (Общие активы / Собственный капитал владельца)
    def getAssetsToEquaityRatio(self):
        assetsToEquaityRatio = self.getTotalAssets() / self.getTotalOwnerEquaity()
        return assetsToEquaityRatio

    # Отношение долга к собственному капиталу (Совокупные обязательства / Собственный капитал владельца)
    def getDebtToEquaityRatio(self):
        debtToEquaityRatio = (self.getTotalCurrentLiabilities() + self.getTotalLongTermLiabilities()) / self.getTotalOwnerEquaity()
        return debtToEquaityRatio




