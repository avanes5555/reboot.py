import datetime
import allure

from libfptr10 import IFptr
import time
now = datetime.datetime.now()
fptr = IFptr('')
#(r'C:\Program Files (x86)\ATOL\Drivers10\KKT\bin\fptr10.dll')
version = fptr.version()
print(version)

fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_MODEL, str(IFptr.LIBFPTR_MODEL_ATOL_AUTO))
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_PORT, str(IFptr.LIBFPTR_PORT_USB))
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_OFD_CHANNEL, str(IFptr.LIBFPTR_OFD_CHANNEL_AUTO))
fptr.setSingleSetting(IFptr.LIBFPTR_SETTING_VALIDATE_MARK_WITH_FNM_ONLY, str("0"))
#fptr.applySingleSettings()
if fptr.applySingleSettings() < 0:
	print("{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))

if fptr.open() < 0:
	print("создать объект","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))
#вывести версию используемой библиотеки драйвера
print(fptr.version())
print()
#вывести версию ФФД
fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_FFD_VERSIONS)
fptr.fnQueryData()
d= fptr.getParamInt(IFptr.LIBFPTR_PARAM_FN_FFD_VERSION)
print("версия ФФД: ", d)
#проверить и вывести статус смены
fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_STATUS)
fptr.queryData()
shiftState      = fptr.getParamInt(IFptr.LIBFPTR_PARAM_SHIFT_STATE)
print("состояние смены: ",shiftState)
#если смена закрыта, то открыть её
if shiftState ==0:
	fptr.openShift()
#если смена истекла, то закрыть и открыть её для продолжения работы скрипта
elif shiftState == 2:
	fptr.setParam (fptr.LIBFPTR_PARAM_REPORT_ELECTRONICALLY, False)
	fptr.setParam (IFptr.LIBFPTR_PARAM_REPORT_TYPE, 0)
	if fptr.report () < 0:
		print ("{} [{}]".format (fptr.errorCode (), fptr.errorDescription ()))
	fptr.openShift ()


def check():
	fptr.setParam(1021, "Кассир Иванов И.")
	fptr.setParam(1203, "123456789047")
	fptr.operatorLogin()

	fptr.setParam(IFptr.LIBFPTR_PARAM_RECEIPT_TYPE, IFptr.LIBFPTR_RT_SELL)
	fptr.openReceipt()
	fptr.setParam(IFptr.LIBFPTR_PARAM_COMMODITY_NAME,
					  "ГАСТРОБЕНЕ ПЛЮС ТАБЛЕТКИ ЖЕВАТЕЛЬНЫЕ №18(КЕНДИ)(2202057; до 01.02.2024")
	fptr.setParam(IFptr.LIBFPTR_PARAM_PRICE, 100)
	fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 5.00)
	fptr.setParam(IFptr.LIBFPTR_PARAM_TAX_TYPE, IFptr.LIBFPTR_TAX_VAT0)
	fptr.registration()
	fptr.setParam(IFptr.LIBFPTR_PARAM_PAYMENT_TYPE, IFptr.LIBFPTR_PT_CASH)
	fptr.setParam(IFptr.LIBFPTR_PARAM_PAYMENT_SUM, 500.00)
	fptr.payment()
	fptr.setParam(IFptr.LIBFPTR_PARAM_PAYMENT_TYPE, IFptr.LIBFPTR_PT_ELECTRONICALLY)
	fptr.closeReceipt()


	while fptr.checkDocumentClosed() < 0:
		# Не удалось проверить состояние документа. Вывести пользователю текст ошибки, попросить устранить неполадку и повторить запрос
		print(fptr.errorDescription())
		continue


	if not fptr.getParamBool(IFptr.LIBFPTR_PARAM_DOCUMENT_CLOSED):
		# Документ не закрылся. Требуется его отменить (если это чек) и сформировать заново
		fptr.cancelReceipt()
		return

	if not fptr.getParamBool(IFptr.LIBFPTR_PARAM_DOCUMENT_PRINTED):
		# Можно сразу вызвать метод допечатывания документа, он завершится с ошибкой, если это невозможно
		while fptr.continuePrint() < 0:
			# Если не удалось допечатать документ - показать пользователю ошибку и попробовать еще раз.
			print('Не удалось напечатать документ (Ошибка "%s"). Устраните неполадку и повторите.',
				  fptr.errorDescription())
			continue
	fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_LAST_DOCUMENT)
	fptr.fnQueryData()
	#time.sleep(1)
	fptr.setParam(IFptr.LIBFPTR_PARAM_FN_DATA_TYPE, IFptr.LIBFPTR_FNDT_SHIFT)
	fptr.fnQueryData()

	fptr.clearMarkingCodeValidationResult()
	print("очистить буффер КМ в ФН ", "{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))


	#отмена проверки КМ, если она запускалась ранее и не была прервана
	#fptr.cancelMarkingCodeValidation()
	#очистить буфер ФН
	#fptr.clearMarkingCodeValidationResult()
	#print("очистить буффер КМ в ФН ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))


mark ="010978500057905321;FgfpT!S(oc%'91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest"
mark1 = '010978500057905321TK4dJIT?teITF91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
mark2 = '0104600266014870217837800520000093xJ8T24010117837'
#'блок сигарет 0104600266014870217837800520000093xJ8T24010117837'
# обувь выбытая реальная 010465013408039121U:iGGBRn!saBX91803992nphGZioHSFOpaUXWpXz+Al6iOcm/cNjish4tTaw4z/wtPGks4+CY4TXzrCKLDveW8l5KPYz6XsA/mUHIq24svA==
#'014494550435306821QXYXSALGLMYQQ\u001D91EE06\u001D92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c='
#'04606203096749jKpjN:ZACgOOcEM'
#'014494550435306821QXYXSALGLMYQQ\u001D91EE06\u001D92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c='
#'015175404137639621Pg0R4Vcxuarsu91ffd092tHvxvNv2hZna+QJefLW+4th9wmu04kwn0yPNJ/xWO9U='
#'010978500057905321;FgfpT!S(oc%'91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
#'014494550435306821QXYXSALGLMYQQ\u001D91EE06\u001D92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c='
#'014494550435306821QXYXSALGLMYQQ{FNC1}91EE06{FNC1}92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c='
#'010978500057905321TK4dJIT?teITF91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
#'010978500057905321TK4dJIT?teITF{FNC1}91FFD0{FNC1}92testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
#'010978500057905321:HJklO%Bm=lqF91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
#'010978500057905321Z?W'*kf=Yo"2h91FFD092testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest'
#'014494550435306821QXYXSALGLMYQQ↔91EE06↔92YWCXbmK6SN8vvwoxZFk7WAY8WoJNMGGr6Cgtiuja04c='
status = 1
status1 = 1
status2 = 1
for i in range (1112):
	# Запускаем проверку КМ1
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_TYPE, IFptr.LIBFPTR_MCT12_AUTO)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark)#2000 код маркировки
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status)#2003 предполагаемый статус
	#fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023 количество, передается если статус товара 2 или 4
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108 мера количества, передается если статус товара 2 или 4
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_WAIT_FOR_VALIDATION_RESULT, True) #ожидать ответа от сервера
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0) #2102 всегда 0
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291 состоит из 1292 - дробная часть (заполняется автоматом из 1293 и 1294), 1293 - числитель, 1294 - знаменатель
	if fptr.beginMarkingCodeValidation():
			print("Запускаем проверку КМ1 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	while True:
			time.sleep(1)
			fptr.getMarkingCodeValidationStatus()
			print ("текущий статус проверки КМ1 ", "{} [{}]".format (fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR), IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR_DESCRIPTION), now)
			if fptr.getParamBool(IFptr.LIBFPTR_PARAM_MARKING_CODE_VALIDATION_READY):
				break
	validationResult = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_RESULT)

	print("результат проверки КМ1 (тег 2106): ",validationResult,now)
	# Подтверждаем реализацию товара с указанным КМ
	fptr.acceptMarkingCode()
	print("Подтверждаем реализацию товара с указанным КМ1 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))

	# Запускаем проверку КМ2
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_TYPE, IFptr.LIBFPTR_MCT12_AUTO)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark1)#2000 код маркировки
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status1)#2003 предполагаемый статус
	#fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023 количество, передается если статус товара 2 или 4
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108 мера количества, передается если статус товара 2 или 4
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_WAIT_FOR_VALIDATION_RESULT, True) #ожидать ответа от сервера
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0) #2102 всегда 0
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291 состоит из 1292 - дробная часть (заполняется автоматом из 1293 и 1294), 1293 - числитель, 1294 - знаменатель
	if fptr.beginMarkingCodeValidation():
			print("Запускаем проверку КМ2 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	while True:
			time.sleep(1)
			fptr.getMarkingCodeValidationStatus()
			print ("текущий статус проверки КМ2 ", "{} [{}]".format (fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR), IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR_DESCRIPTION),now)
			if fptr.getParamBool(IFptr.LIBFPTR_PARAM_MARKING_CODE_VALIDATION_READY):
				break
	validationResult1 = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_RESULT)

	print("результат проверки КМ2 (тег 2106): ", validationResult1,now)
	# Подтверждаем реализацию товара с указанным КМ
	fptr.acceptMarkingCode()
	print("Подтверждаем реализацию товара с указанным КМ2 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	#Запускаем проверку КМ3
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_TYPE, IFptr.LIBFPTR_MCT12_AUTO)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark2)#2000 код маркировки
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status2)#2003 предполагаемый статус
	#fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023 количество, передается если статус товара 2 или 4
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108 мера количества, передается если статус товара 2 или 4
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_WAIT_FOR_VALIDATION_RESULT, True) #ожидать ответа от сервера
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0) #2102 всегда 0
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291 состоит из 1292 - дробная часть (заполняется автоматом из 1293 и 1294), 1293 - числитель, 1294 - знаменатель
	if fptr.beginMarkingCodeValidation():
			print("Запускаем проверку КМ3 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	while True:
			time.sleep(1)
			fptr.getMarkingCodeValidationStatus()
			print ("текущий статус проверки КМ3 ", "{} [{}]".format (fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR), IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_ERROR_DESCRIPTION),now)
			if fptr.getParamBool(IFptr.LIBFPTR_PARAM_MARKING_CODE_VALIDATION_READY):
				break
	validationResult2 = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MARKING_CODE_ONLINE_VALIDATION_RESULT)

	print("результат проверки КМ3 (тег 2106): ",validationResult2,now)
	# Подтверждаем реализацию товара с указанным КМ
	fptr.acceptMarkingCode()
	print("Подтверждаем реализацию товара с указанным КМ3 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	#Формируем чек
	#Открыть чек
	fptr.setParam(IFptr.LIBFPTR_PARAM_RECEIPT_TYPE, IFptr.LIBFPTR_RT_SELL)
	fptr.setParam(IFptr.LIBFPTR_PARAM_RECEIPT_ELECTRONICALLY, True)
	if fptr.openReceipt() < 0:
		print("Открываем чек ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))

	#Позиция 1
	fptr.setParam(IFptr.LIBFPTR_PARAM_COMMODITY_NAME, 'Позиция чека №1')
	fptr.setParam(IFptr.LIBFPTR_PARAM_PRICE, 80.5)
	fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291
	fptr.setParam(IFptr.LIBFPTR_PARAM_TAX_TYPE, IFptr.LIBFPTR_TAX_VAT10)
	fptr.setParam(1212, 33)
	fptr.setParam(1214, 4)
	fptr.setParam(2108, 0)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark) #1163
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status)
	fptr.setParam(2106, validationResult)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0)
	if fptr.registration() < 0:
		print("регистрация позиции 1 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	#Позиция 2
	fptr.setParam(IFptr.LIBFPTR_PARAM_COMMODITY_NAME, 'Позиция чека №2')
	fptr.setParam(IFptr.LIBFPTR_PARAM_PRICE, 50)
	fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291
	fptr.setParam(IFptr.LIBFPTR_PARAM_TAX_TYPE, IFptr.LIBFPTR_TAX_VAT10)
	fptr.setParam(1212, 33)
	fptr.setParam(1214, 4)
	fptr.setParam(2108, 0)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark1) #1163
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status1)
	fptr.setParam(2106, validationResult1)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0)
	if fptr.registration() < 0:
		print("регистрация позиции 2 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	#Позиция 3
	fptr.setParam(IFptr.LIBFPTR_PARAM_COMMODITY_NAME, 'Позиция чека №3')
	fptr.setParam(IFptr.LIBFPTR_PARAM_PRICE, 120)
	fptr.setParam(IFptr.LIBFPTR_PARAM_QUANTITY, 1.000) #1023
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MEASUREMENT_UNIT, 0) #2108
	#fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_FRACTIONAL_QUANTITY, '1/2') #1291
	fptr.setParam(IFptr.LIBFPTR_PARAM_TAX_TYPE, IFptr.LIBFPTR_TAX_VAT20)
	fptr.setParam(1212, 33)
	fptr.setParam(1214, 4)
	fptr.setParam(2108, 0)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE, mark2) #1163
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_CODE_STATUS, status2)
	fptr.setParam(2106, validationResult2)
	fptr.setParam(IFptr.LIBFPTR_PARAM_MARKING_PROCESSING_MODE, 0)
	if fptr.registration() < 0:
		print("регистрация позиции 3 ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)

	if fptr.closeReceipt() < 0:
		print("Закрыть чек ","{} [{}]".format(fptr.errorCode(), fptr.errorDescription()),now)
		if fptr.errorCode() == 203:
			fptr.cancelReceipt()
			print("документ отменен",now)
	def readNextRecord(fptr, recordsID):
		fptr.setParam(IFptr.LIBFPTR_PARAM_RECORDS_ID, recordsID)
		return fptr.readNextRecord()


	fptr.setParam(IFptr.LIBFPTR_PARAM_RECORDS_TYPE, IFptr.LIBFPTR_RT_FN_DOCUMENT_TLVS)
	fptr.setParam(IFptr.LIBFPTR_PARAM_DOCUMENT_NUMBER, 157)
	fptr.beginReadRecords()
	documentType = fptr.getParamInt(IFptr.LIBFPTR_PARAM_FN_DOCUMENT_TYPE)
	documentSize = fptr.getParamInt(IFptr.LIBFPTR_PARAM_COUNT)
	recordsID = fptr.getParamString(IFptr.LIBFPTR_PARAM_RECORDS_ID)

	while readNextRecord(fptr, recordsID) == IFptr.LIBFPTR_OK:
		tagValue = fptr.getParamByteArray(IFptr.LIBFPTR_PARAM_TAG_VALUE)
		tagNumber = fptr.getParamInt(IFptr.LIBFPTR_PARAM_TAG_NUMBER)
		tagName = fptr.getParamString(IFptr.LIBFPTR_PARAM_TAG_NAME)
		tagType = fptr.getParamInt(IFptr.LIBFPTR_PARAM_TAG_TYPE)

	fptr.setParam(IFptr.LIBFPTR_PARAM_RECORDS_ID, recordsID)
	fptr.endReadRecords()



	
	check()
	fptr.clearMarkingCodeValidationResult()
	print("очистить буффер КМ в ФН ", "{} [{}]".format(fptr.errorCode(), fptr.errorDescription()))





