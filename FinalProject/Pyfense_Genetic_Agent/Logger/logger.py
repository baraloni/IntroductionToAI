import sys
import os
import csv
import json
from GeneticAgent.config import SOL_IN_PATH

class Logger:

    """
    The Logger class is used to save the data of the Genetic Agent runs
    """

    CSV_HEADER = ["Generation", "ID", "Fitness", "Lives lost", "Money earned", "Money spent", "Waves Survived"]

    def __init__(self):

        self.main_directory_path = self.create_main_directory()
        self.run_log = open(os.path.join(self.main_directory_path, "run.log"), 'w')
        self.segment_cvs_files = list()
        self.current_segment = -1

        print("The logs to this run may be found under directory:")
        print(self.main_directory_path)


    def create_main_directory(self):
        """
        Creates the directory where all files for the run are saved 
        """
        path = os.getcwd()
        logs_dir = os.path.join(path,"Logger", "run_logs")

        i = 0
        while os.path.exists(logs_dir + "." + str(i)):
            i += 1

        logs_dir = logs_dir + "." + str(i)
        os.mkdir(logs_dir)

        return logs_dir


    def create_segment_csv(self):
        """
        Create the csv of the segment and write header
        """
        self.current_segment += 1
        path = self.get_csv_file_name()
        self.segment_cvs_files.append(path)

        with open(path, 'a+', newline ='') as file:
            csv.writer(file).writerow(self.CSV_HEADER)


    def end_run(self):
        self.run_log.close()


    def write_to_run_log(self, data):
        """
        file need to be open as writeable
        """
        self.run_log.write(data + "\n")


    def write_run_parameters(self, pop_size, gen_num, fit_num, mut_rate, init_money, seg_num, waves_per_seg):
        """
        @param::pop_size - size of population per generation
        @param::gen_num - number of genrations to learn each segment
        @param::fit_num - number of fittest to create next generation
        @param::mut_rate - mutation rate
        @param::init_money - initial money to start the first segment with
        @param::seg_num - number of segments to try and learn
        @param::waves_per_seg - how many waves to learn per segment
        """
        s = ["This run parameters are:\n"]

        # Algorithm parameters
        s.append("  Algorithm parameters:")
        s.append("      Population size: " + str(pop_size))
        s.append("      Fittest individuals amount after selection: " + str(fit_num))
        s.append("      Number of generations per segment: " + str(gen_num))
        s.append("      Mutation Rate: " + str(mut_rate) + "\n")       

        # Game parameters
        s.append("  Game parameters:")
        s.append("      Money at the start of the game: " + str(init_money))
        s.append("      Number of segments to learn: " + str(seg_num))
        s.append("      Number of waves per segment: " + str(waves_per_seg) + "\n")
        
        s.append("Starting the run!\n\n")

        for line in s:
            self.write_to_run_log(line)


    def save_segment_execution_time(self, seg_num, time):
        """
        @param::seg_num - segment number
        @param::time - time it took to learn segment
        @param::avrg_fitns - average fitness of the last generation of the segment
        @param::high_fitns - highest fitness of the last generation of the segment
        """
        self.write_to_run_log("Learned segment " + str(seg_num) + " in (hh:mm:ss.ms) {}".format(time) + "\n")


    def save_generation_summary(self, gen_num, avrg_fitns, high_fitns):
        """
        @param::gen_num - generation number
        @param::avrg_fitns - average fitness of the last generation of the segment
        @param::high_fitns - highest fitness of the last generation of the segment
        """
        self.write_to_run_log("Fitness of generation " + str(gen_num) + " - average: " + 
                                        str(avrg_fitns) + " highest: "  + str(high_fitns))


    def write_failure_message(self, seg_num):
        """
        @param::seg_num - segment number
        """
        self.write_to_run_log("The run terminated because no fittest who passed the segment remained")


    def save_generation_data(self, data):
        """
        @param::data - data to save, list of lists(generation, id, fitness, money earned, money spent, lives lost, waves survived)
        """
        with open(self.segment_cvs_files[self.current_segment], 'a+', newline ='') as file:
            write = csv.writer(file) 
            write.writerows(data)


    def get_csv_file_name(self):
        """
        Returns the name of the file
        """
        path = os.path.join(self.main_directory_path, "segment_" + str(self.current_segment) + ".csv")
        return path


    def log_solutions(self, solutions):
        """
        @param::solutions - list of genomes to save
        """
        with open(SOL_IN_PATH, 'w') as f:
            json.dump(solutions, f)


