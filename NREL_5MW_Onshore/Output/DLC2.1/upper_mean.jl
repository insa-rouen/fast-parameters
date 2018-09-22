# Calculate the mean of upper extreme values
# Hao BAI
# 22/09/2018

import CSV
import Statistics

function upper_mean(file)
    # read data from file
    data = CSV.read(file, header=7, datarow=6009, delim="\t")
    header = names(data) # get column names
    colnumbers = length(header)
    # calculate median value for each column
    medians = CSV.colwise(Statistics.median, data)
    # select values greater than median
    upper = [ data[data[:,i].≥medians[i],:] for i in (1:colnumbers)]
    # calculate mean of half largest values
    means = [Statistics.mean(upper[i][:,i]) for i in (1:colnumbers)]

    return means, header
end


files = (
         "NTM_11mps_-1275024443.out",
         "NTM_11mps_-1636941546.out",
         # "NTM_11mps_-1735756529.out",
         # "NTM_11mps_-338643755.out",
         # "NTM_11mps_1089003891.out",
         # "NTM_11mps_1129452413.out",
         # "NTM_11mps_114549328.out",
         # "NTM_11mps_1221357172.out",
         # "NTM_11mps_126985980.out",
         # "NTM_11mps_1587273680.out",
         # "NTM_11mps_2033616203.out",
         # "NTM_11mps_2134726005.out",
         # "NTM_13mps_-1072360737.out",
         # "NTM_13mps_-1956845479.out",
         # "NTM_13mps_-2005772928.out",
         # "NTM_13mps_-2139873620.out",
         # "NTM_13mps_-558067084.out",
         # "NTM_13mps_-69386907.out",
         # "NTM_13mps_1608998667.out",
         # "NTM_13mps_1614676674.out",
         # "NTM_13mps_1798309968.out",
         # "NTM_13mps_2079440682.out",
         # "NTM_13mps_329691992.out",
         # "NTM_13mps_668533241.out",
         # "NTM_15mps_-1157782067.out",
         # "NTM_15mps_-1334923788.out",
         # "NTM_15mps_-1342629666.out",
         # "NTM_15mps_-340277597.out",
         # "NTM_15mps_-347435842.out",
         # "NTM_15mps_-407950422.out",
         # "NTM_15mps_-655151327.out",
         # "NTM_15mps_1340439326.out",
         # "NTM_15mps_2046979483.out",
         # "NTM_15mps_726969154.out",
         # "NTM_15mps_771000393.out",
         # "NTM_15mps_810128860.out",
         # "NTM_17mps_-1694870869.out",
         # "NTM_17mps_-1897228120.out",
         # "NTM_17mps_-1928254863.out",
         # "NTM_17mps_-2044436073.out",
         # "NTM_17mps_-2143090490.out",
         # "NTM_17mps_-656307010.out",
         # "NTM_17mps_-699129187.out",
         # "NTM_17mps_-923870650.out",
         # "NTM_17mps_1465409576.out",
         # "NTM_17mps_420049665.out",
         # "NTM_17mps_537417508.out",
         # "NTM_17mps_633993940.out",
         # "NTM_19mps_-1684990063.out",
         # "NTM_19mps_-1922709128.out",
         # "NTM_19mps_-2865845.out",
         # "NTM_19mps_1077766457.out",
         # "NTM_19mps_1365652430.out",
         # "NTM_19mps_159530534.out",
         # "NTM_19mps_1851326851.out",
         # "NTM_19mps_223013459.out",
         # "NTM_19mps_353520954.out",
         # "NTM_19mps_459444760.out",
         # "NTM_19mps_741781101.out",
         # "NTM_19mps_80550771.out",
         # "NTM_21mps_-1043280086.out",
         # "NTM_21mps_-1749714001.out",
         # "NTM_21mps_-656002684.out",
         # "NTM_21mps_-824922898.out",
         # "NTM_21mps_1151458495.out",
         # "NTM_21mps_156595434.out",
         # "NTM_21mps_181688646.out",
         # "NTM_21mps_2025699203.out",
         # "NTM_21mps_2051817524.out",
         # "NTM_21mps_205306756.out",
         # "NTM_21mps_389956739.out",
         # "NTM_21mps_935626405.out",
         # "NTM_23mps_-107423970.out",
         # "NTM_23mps_-1621912599.out",
         # "NTM_23mps_-188411971.out",
         # "NTM_23mps_-556149176.out",
         # "NTM_23mps_-945276968.out",
         # "NTM_23mps_1046559425.out",
         # "NTM_23mps_1467335172.out",
         # "NTM_23mps_172104750.out",
         # "NTM_23mps_1802968337.out",
         # "NTM_23mps_302621303.out",
         # "NTM_23mps_36387814.out",
         # "NTM_23mps_52346169.out",
         # "NTM_25mps_-1491237681.out",
         # "NTM_25mps_-1774975822.out",
         # "NTM_25mps_-178479734.out",
         # "NTM_25mps_-786458077.out",
         # "NTM_25mps_-921159385.out",
         # "NTM_25mps_-935044776.out",
         # "NTM_25mps_1042376567.out",
         # "NTM_25mps_1624172648.out",
         # "NTM_25mps_2009940885.out",
         # "NTM_25mps_2123365223.out",
         # "NTM_25mps_42484554.out",
         # "NTM_25mps_877739847.out",
         # "NTM_3mps_-1040692495.out",
         # "NTM_3mps_-1135038058.out",
         # "NTM_3mps_-148075506.out",
         # "NTM_3mps_-323429266.out",
         # "NTM_3mps_-615392578.out",
         # "NTM_3mps_1049798192.out",
         # "NTM_3mps_129389219.out",
         # "NTM_3mps_1506317300.out",
         # "NTM_3mps_2088699444.out",
         # "NTM_3mps_533663769.out",
         # "NTM_3mps_80167948.out",
         # "NTM_3mps_888802706.out",
         # "NTM_5mps_-1452941866.out",
         # "NTM_5mps_-1494309489.out",
         # "NTM_5mps_-1517588562.out",
         # "NTM_5mps_-218443567.out",
         # "NTM_5mps_-594378616.out",
         # "NTM_5mps_1216316837.out",
         # "NTM_5mps_1341097192.out",
         # "NTM_5mps_1508518028.out",
         # "NTM_5mps_211128746.out",
         # "NTM_5mps_387049032.out",
         # "NTM_5mps_846291.out",
         # "NTM_5mps_90624527.out",
         # "NTM_7mps_-1252303864.out",
         # "NTM_7mps_-1895365015.out",
         # "NTM_7mps_-1949965055.out",
         # "NTM_7mps_-289045182.out",
         # "NTM_7mps_1584186825.out",
         # "NTM_7mps_1957237072.out",
         # "NTM_7mps_2137104168.out",
         # "NTM_7mps_290393834.out",
         # "NTM_7mps_306993512.out",
         # "NTM_7mps_51377197.out",
         # "NTM_7mps_617552194.out",
         # "NTM_7mps_888775382.out",
         # "NTM_9mps_-1302288173.out",
         # "NTM_9mps_-188183563.out",
         # "NTM_9mps_-1890866586.out",
         # "NTM_9mps_-2112011771.out",
         # "NTM_9mps_-2114264661.out",
         # "NTM_9mps_-220782676.out",
         # "NTM_9mps_-496198015.out",
         # "NTM_9mps_1512186763.out",
         # "NTM_9mps_1564563718.out",
         # "NTM_9mps_1753282896.out",
         # "NTM_9mps_185958074.out",
         # "NTM_9mps_1982094552.out",
        )

file="NTM_11mps_-1275024443.out"
mean, header = upper_mean(file)
df = CSV.DataFrame(mean, header)
push!(df, mean)

file = "NTM_11mps_-1636941546.out"
mean, header = upper_mean(file)
# df = CSV.DataFrame(mean)
push!(df, mean)
# for file in files
#     mean, header = upper_mean(file)
#     df = CSV.DataFrame(mean, header)
# end


CSV.write("result.avg", df; delim='\t')
