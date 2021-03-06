# -*- coding: UTF-8 -*- 
import re

ddlstr="""
CREATE TABLE `user`
(
    `id`            bigint      NOT NULL AUTO_INCREMENT COMMENT '主键',
    `name`     bigint      NOT NULL COMMENT '姓名',
    `age`    varchar(64) NOT NULL COMMENT '年龄',
    `valid_sign`    tinyint     NOT NULL DEFAULT '1' COMMENT '是否有效：1有效，0无效',
    `created_date`  datetime    NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `modified_date` timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8
  COLLATE = utf8_bin COMMENT ='用户表';

"""

daopackage='com.jd.jr.plutus.products.finance.dao'

def typeToJava(sqlType):
	sqlType = sqlType.lower()
	if sqlType.startswith("bigint"):
		return 'Long';
	if sqlType.startswith("varchar"):
		return 'String';
	if sqlType.startswith("decimal"):
		return 'BigDecimal';
	if sqlType.startswith("int"):
		return 'Integer';
	if sqlType.startswith("tinyint"):
		return 'Integer';
	if sqlType.startswith("datetime"):
		return 'Date';
	if sqlType.startswith("timestamp"):
		return 'Date';
	return sqlType

def columnToName(column):
	arr = column.split("_")
	for i in range(len(arr)):
		if i > 0:
			arr[i] = arr[i].capitalize()
		else:
			arr[i] = arr[i]
	column = ''.join(arr)
	return column

def tableToClassName(column):
	arr = column.split("_")
	arr = [arr[i].capitalize() for i in range(len(arr))]
	return ''.join(arr)



tis = ddlstr.find("`")+1
table_name = ddlstr[tis: ddlstr.find("`",tis)]
classname =tableToClassName(table_name)
description = ddlstr[ddlstr.rfind("'" , 0 ,ddlstr.rfind("'") -1)+1 :ddlstr.rfind("'")].replace("表","")
ddlstr = ddlstr[ddlstr.find("(")+1:ddlstr.rfind(")")-1]

arr = ddlstr.split("',")



nameArr =[]
columnArr =[]

print("============================== entity start =========================== \n")
for item in arr:
	if item.find('PRIMARY') != -1:
		break

	subArr =item.strip().split(" ")
	#print(subArr)
	column = subArr[0].strip().replace("`" , "")
	name = columnToName(column)
	columnArr.append(column)
	nameArr.append(name)
	print("/** %s */" %(subArr[-1].replace("'" , "").strip())+"\n"+"private %s %s;" %(typeToJava(subArr[1].strip()),name)) 

print("============================== entity end =========================== \n")

print("============================== mapper java start ===========================")
print("/**\n * 插入%s \n * @param record \n */\nvoid save(%s record);" %(description , classname))
print("/**\n * 更新%s \n * @param updater \n */\nvoid update(%s updater);" %(description , classname))
print("/**\n * 根据条件查询单条%s记录 \n * @param criteria \n */\n%s getOneBySelective(%sCriteria criteria);" %(description , classname , classname))
print("/**\n * 根据条件查询多条%s记录 \n * @param criteria \n */\n List<%s> getListBySelective(%sCriteria criteria);" %(description , classname , classname))
print("============================== mapper java end =========================== \n")


print("============================== mapper xml start ===========================\n")

sqlColumns=[columnArr[i] + ' as ' + nameArr[i] for i in range(len(columnArr))]
print( "<sql id=\"Base_Column_List\">\n\t" + ",\n\t".join(sqlColumns) + "\n</sql>\n")

columnArr.remove("id")
columnArr.remove("created_date")
columnArr.remove("modified_date")
nameArr.remove("id")
nameArr.remove("createdDate")
nameArr.remove("modifiedDate")



sqlInsertNames =["#{%s}" % (nameArr[i]) for i in range(len(nameArr) -1)]
print("<insert id=\"save\" parameterType=\"%s.entity.%s\">\n\tINSERT INTO %s (\n\t\t%s\n\t) VALUES (\n\t\t%s\n\t)\n</insert>\n" %(daopackage , classname , table_name ,",\n\t\t".join(columnArr[0 :len(columnArr) - 1]) ,",\n\t\t".join(sqlInsertNames)))

sqlUpdate = []
updateExclude=["channelCode","userId"]
for i in range(len(nameArr)):
	if nameArr[i] in updateExclude :
		continue
	if i == len(nameArr)-1 :
		sqlUpdate.append("\t\t<if test=\"null != %s\">\n\t\t\t%s = #{%s}\n\t\t</if>" %(nameArr[i],columnArr[i],nameArr[i]))
	else:
		sqlUpdate.append("\t\t<if test=\"null != %s\">\n\t\t\t%s = #{%s},\n\t\t</if>" %(nameArr[i],columnArr[i],nameArr[i]))

print("<update id=\"update\" parameterType=\"%s.entity.%s\">\n\tUPDATE %s \n\t<set>\n%s\n\t</set>\n\tWHERE id = #{id}\n</update>\n" %(daopackage , classname , table_name,"\n".join(sqlUpdate)))

sqlCriteria = ["\t\t<if test=\"null != bean.id\">\n\t\t\tand id = #{bean.id}\n\t\t</if>"]
sqlCriteria = sqlCriteria + ["\t\t<if test=\"null != bean.%s\">\n\t\t\tand %s = #{bean.%s}\n\t\t</if>" %(nameArr[i],columnArr[i],nameArr[i]) for i in range(len(nameArr))]
print("<sql id=\"Dynamic_Bean_Criteria\">\n\t<if test=\"null != bean\">\n%s\n\t</if>\n</sql>" %("\n".join(sqlCriteria)))


print("<select id=\"getOneBySelective\" parameterType=\"%s.criteria.%sCriteria\"\n\tresultType=\"%s.entity.%s\">\n\tSELECT\n\t<include refid=\"Base_Column_List\"/>\n\tFROM %s\n\twhere valid = 1\n\t<include refid=\"Dynamic_Bean_Criteria\"/>\n</select>" %(daopackage , classname , daopackage , classname , table_name)) 

print("<select id=\"getListBySelective\" parameterType=\"%s.criteria.%sCriteria\"\n\tresultType=\"%s.entity.%s\">\n\tSELECT\n\t<include refid=\"Base_Column_List\"/>\n\tFROM %s\n\twhere valid = 1\n\t<include refid=\"Dynamic_Bean_Criteria\"/>\n\t<if test=\"sort != null and sort.size() > 0\">\n\t\t<foreach collection=\"sort\" open=\" order by \" separator=\" , \" item=\"sortItem\">\n\t\t\t${sortItem.filed} ${sortItem.type}\n\t\t</foreach>\n\t</if>\n\t<if test=\"null != pageStartNum and null != pageSize\">\n\t\tlimit #{pageStartNum},#{pageSize}\n\t</if>\n</select>" %(daopackage , classname , daopackage , classname , table_name)) 
print("============================== mapper xml end ===========================")



setterUtil=["dest.set%s(sorc.get%s())" %(nameArr[i][0].capitalize() + nameArr[i][1:],nameArr[i][0].capitalize() + nameArr[i][1:]) for i in range(len(columnArr))]
print(";\n".join(setterUtil));