import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path
import pathlib

np.set_printoptions(suppress=True)

# test paths:
# /Users/basti/PycharmProjects/Bachelorthesis/Data/Active/test_import.xlsx
# /Users/basti/PycharmProjects/Bachelorthesis/Data/Active/DWS_VermoegensB.xlsx
# /Users/basti/PycharmProjects/Bachelorthesis/Data/Benchmark/MSCI_WORLD_raw.xlsx
# /Users/basti/PycharmProjects/Bachelorthesis/Data/Active/unifonds.xlsx
# /Users/basti/PycharmProjects/Bachelorthesis/Data/Active/UniGlobal.xlsx

final_df = pd.DataFrame()
perf_comb = pd.DataFrame()

### set duration of savings plan in months
# 5y = 59
# 10y = 119
# 15y = 179
# 20y = 239
# 25y = 299
# 30y = 358
duration=59


directory = '/Users/basti/PycharmProjects/Bachelorthesis/Data/TestRun/'

for filename in os.scandir(directory):
    if filename.is_file():

        print('#################################################')
        print('#################################################')
        print('start analysis for ', pathlib.Path(filename).name)
        print('#################################################')
        print('#################################################')

        print("current file: ", pathlib.Path(filename).name)
        current_file = filename.path

        df = pd.read_excel(current_file)

        # calculate change in % and add column
        df['delta'] = ((df.iloc[:,-1] - df.iloc[:,-1].shift(1)) / df.iloc[:,-1].shift(1))

        # create performance array
        perf = np.array([])

        # investing at beginning of month, drop first value bc no percentage change DELETE THIS if investment at end of month
        df = df.iloc[1:, :]
        print(df)

        # save changes in separate list
        changes = df.iloc[:, -1]


        # simulate rolling savings plan
        for x in range(len(changes) - duration):
                # start savings plan list with initial value (first record got dropped so 2nd is first used value)
                values = np.array([100 * (df.iloc[x, -1] + 1)])

                # one savings plan
                for i in range(duration):
                        values = np.append(values, (values[i]+100)*(df.iloc[x+i+1,-1]+1))

                # assign final return values to according result arrays
                perf = np.append(perf, values[-1] / ((duration + 1) * 100))

                # reset value array and inner_count
                values = np.array([])



###############################################################################################
################################ calculate perf for MSCI World ################################
###############################################################################################
######################## no fund should have longer history than MSCI #########################
###############################################################################################

        BENCHMARK_df = pd.read_excel('/Users/basti/PycharmProjects/Bachelorthesis/Data/Benchmark/MSCI_WORLD_raw.xlsx')
        # calculate change in % and add column
        BENCHMARK_df['change in %'] = (
                        (BENCHMARK_df.iloc[:, -1] - BENCHMARK_df.iloc[:, -1].shift(1)) / BENCHMARK_df.iloc[:, -1].shift(
                        1))

        # check if performance arrays already exist, if not create them
        BENCHMARK_perf = np.array([])

        # make sure that fund and MSCI have the same observation period
        diff = BENCHMARK_df.shape[0] - len(changes)

        # investing at beginning of month, drop first value bc no percentage change DELETE THIS if investment at end of month
        BENCHMARK_df = BENCHMARK_df.iloc[diff:, :]

        # save changes in separate list
        BENCHMARK_changes = BENCHMARK_df.iloc[:, -1]

        print("length of fund: ", len(changes))
        print("length of benchmark: ", len(BENCHMARK_changes))



        for x in range(len(BENCHMARK_changes) - duration):
                # start savings plan list with initial value (first record got dropped so 2nd is first used value)
                BENCHMARK_values = np.array([100 * (BENCHMARK_df.iloc[x, -1] + 1)])

                # one savings plan
                for i in range(duration):
                        BENCHMARK_values = np.append(BENCHMARK_values, (BENCHMARK_values[i]+100)*(BENCHMARK_df.iloc[x+i+1,-1]+1))

                # assign final return values to according result arrays
                BENCHMARK_perf = np.append(BENCHMARK_perf, BENCHMARK_values[-1] / ((duration + 1) * 100))

                # reset value array and inner_count
                BENCHMARK_values = np.array([])

        # print('#################################################')
        # print('#################################################')
        # print("Benchmark perf: ", pathlib.Path(filename).name,BENCHMARK_perf)
        # print("PERF: ", pathlib.Path(filename).name, perf)
        # print('#################################################')
        # print('#################################################')
        print("length of fund: ", len(perf))
        print("length of BENCHMARK_fund: ", len(BENCHMARK_perf))

        print("last value of fund: ", perf[-1])
        print("last value of BENCHMARK_fund: ", BENCHMARK_perf[-1])

        # calculate performance ratio Fund/Benchmark
        ratios = np.divide(perf, BENCHMARK_perf)

        print("mean of ratios: ", np.mean(ratios))

        ratios = np.append(ratios, df.iloc[0,0])
        ratios = np.append(ratios, df.iloc[-1,0])

        #ratios = np.append(ratios, pathlib.Path(filepath).name)

        df_ratios = pd.DataFrame({pathlib.Path(filename).name: ratios})

        final_df = pd.concat([final_df, df_ratios], axis=1)
        print(final_df)

        print('#################################################')
        print('#################################################')
        print('end of analysis for ', pathlib.Path(filename).name)
        print('#################################################')
        print('#################################################')

# sys.exit("STOP")

df_out = pd.DataFrame(final_df)

# calculate means for each row
df_out["mean"] = final_df.mean(axis=1, numeric_only=True)
out_file = '/Users/basti/PycharmProjects/Bachelorthesis/Data/TEST_output_active/out.csv'
df_out.to_csv(out_file, index=False)
print(" ")
print(" ")
print("FINAL RESULT", df_out)
# plt.hist(ratios)
# plt.show()




