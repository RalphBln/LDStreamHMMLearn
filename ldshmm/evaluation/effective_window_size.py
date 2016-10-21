from unittest import TestCase
from ldshmm.util.mm_family import MMFamily1
from ldshmm.util.util_functionality import *
import math
from msmtools.estimation import transition_matrix as _tm
from ldshmm.util.plottings import PointPlot

class Effective_Window_Size_Test(TestCase):
    def setUp(self):

        self.taumeta = 4
        self.shift = 64
        self.num_trajectories = 2
        self.window_size = [int(128*math.pow(2,i)) for i in range (1,7)]
        self.len_trajectory = self.window_size[-1] + 16 * self.shift
        self.num_estimations = 32

    def test_effective_window_size(self):
        avg_err = {}
        avg_err_bayes = {}
        effective_window_size_values=[]
        first_run = True

        for j in range(0,8):
            if j>0:
                first_run=False

            # sample and simulate the trajectory only once for one iteration over the windows values
            self.num_states = 4
            self.mmf1_0 = MMFamily1(self.num_states)
            self.mm1_0_0 = self.mmf1_0.sample()[0]

            self.data1_0_0 = []
            self.mm1_0_0_scaled = self.mm1_0_0.eval(self.taumeta)

            for i in range(0, self.num_trajectories):
                self.data1_0_0.append(self.mm1_0_0_scaled.simulate(int(self.len_trajectory)))
            dataarray = np.asarray(self.data1_0_0)
            err_list = []
            err_bayes_list = []

            for window_size in self.window_size:
                self.r = (window_size - self.shift) / window_size
                if first_run:
                    effective_window_size_values.append(self.shift/(1-self.r))
                err = np.zeros(self.num_estimations + 1, dtype=float)
                errbayes = np.zeros(self.num_estimations + 1, dtype=float)
                try:
                    err, errbayes = self.performance_and_error_calculation(dataarray, err, errbayes, window_size)
                except:
                    self.test_effective_window_size()

                err_list.append(err)
                err_bayes_list.append(errbayes)
            avg_err[j]=err_list
            avg_err_bayes[j]=err_bayes_list

        # calculate mean error
        avg_err_final = np.mean(list(avg_err.values()), axis=0)
        avg_err_bayes_final = np.mean(list(avg_err_bayes.values()), axis=0)

        print(avg_err_final)
        print(avg_err_bayes_final)

        # take the log values
        avg_err_final = [math.log2(x) for x in avg_err_final]
        avg_err_bayes_final = [math.log2(y) for y in avg_err_bayes_final]
        window_size = [math.log2(z) for z in self.window_size]
        effective_window_size_values = [math.log2(a) for a in effective_window_size_values]

        print("Final avg naive errors:",avg_err_final)
        print("Final avg bayes errors:",avg_err_bayes_final)
        plot = PointPlot()
        plot.new_plot("Effective Window Size", rows=1)
        plot.add_data_to_plot(avg_err_final, window_size)
        print(avg_err_final, window_size)
        plot.add_data_to_plot(avg_err_bayes_final, effective_window_size_values)
        print(avg_err_bayes_final, effective_window_size_values)
        plot.save_plot("effective_window_size_plot")

    def performance_and_error_calculation(self, dataarray, err, errbayes, window_size):
        for k in range(0, self.num_estimations + 1):
            data0 = dataarray[:, k * self.shift: (window_size + k * self.shift)]
            dataslice0 = []

            for i in range(0, self.num_trajectories):
                dataslice0.append(data0[i, :])
            if k == 0:
                # init
                estimate_via_sliding_windows(data=dataslice0, num_states=self.num_states)

            C0 = estimate_via_sliding_windows(data=dataslice0, num_states=self.num_states)  # count matrix for whole window
            C0 += 1e-8
            A0 = _tm(C0)
            err[k] = np.linalg.norm(A0 - self.mm1_0_0_scaled.trans)
            if k == 0:
                ##### Bayes approach: Calculate C0 separately
                data0 = dataarray[:, 0 * self.shift: (window_size + 0 * self.shift)]
                dataslice0 = []
                for i in range(0, self.num_trajectories):
                    dataslice0.append(data0[i, :])
                C_old = estimate_via_sliding_windows(data=dataslice0, num_states=self.num_states)
                errbayes[0] = np.linalg.norm(_tm(C_old) - self.mm1_0_0_scaled.trans)

            if k >= 1:
                ##### Bayes approach: Calculate C1 (and any following) usind C0 usind discounting
                data1new = dataarray[:, window_size + (k - 1) * self.shift - 1: (window_size + k * self.shift)]
                dataslice1new = []
                for i in range(0, self.num_trajectories):
                    dataslice1new.append(data1new[i, :])
                C_new = estimate_via_sliding_windows(data=dataslice1new,
                                                     num_states=self.num_states)  # count matrix for just new transitions
                weight0 = self.r
                weight1 = 1.0

                C1bayes = weight0 * C_old + weight1 * C_new
                C_old = C1bayes
                A1bayes = _tm(C1bayes)
                errbayes[k] = np.linalg.norm(A1bayes - self.mm1_0_0_scaled.trans)
        return err[-1], errbayes[-1]