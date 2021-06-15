import sys
from itertools import combinations
import numpy as np


def create_obj_at_obj(o1, o2):
    return "_".join([o1, o2])

def create_disk_less_than_disk(d1, d2):
    return "_".join(["s", d1, d2])

def create_empty_peg(p):
    return "e_" + p

def create_top_disk(d):
    return "f_" + d

def create_ground_disk(d):
    return "g_" + d

def write_move(file, move):
    file.write("Name: " + move[0] + "\n")
    file.write("pre: " + move[1] + "\n")
    file.write("add: " + move[2] + "\n")
    file.write("delete: " + move[3] + "\n")

def alone_to_empty(disk, pre_peg, post_peg):
    # a_d_i_p_j_p_k
    # add move from peg with single disk to empty peg
    name = "_".join(["a", disk, pre_peg, post_peg])
    pre = create_obj_at_obj(disk, pre_peg) + " " + create_top_disk(disk)
    pre += " " + create_ground_disk(disk) + " " + create_empty_peg(post_peg)
    add_props = create_empty_peg(pre_peg) + " " + create_obj_at_obj(disk, post_peg)
    delete_props = create_empty_peg(pre_peg) + " " + create_obj_at_obj(disk, pre_peg)
    return (name, pre, add_props, delete_props)

def disk_to_empty(d1, d2, pre_peg, post_peg):
    # d_i_d_j_p_k_e_p_l
    # add move from peg with multiple disks to empty peg
    name = "_".join([d1, d2, pre_peg, "e", post_peg])
    pre = create_obj_at_obj(d1, d2) + " " + create_obj_at_obj(d1, pre_peg)
    pre += " " + create_top_disk(d1) + " " + create_empty_peg(post_peg)
    add_props = create_top_disk(d2) + " " + create_obj_at_obj(d1, post_peg)
    add_props += " " + create_ground_disk(d1)
    delete_props = create_obj_at_obj(d1, d2) + " " + create_obj_at_obj(d1, pre_peg)
    delete_props += " " + create_empty_peg(post_peg)
    return (name, pre, add_props, delete_props)

def alone_to_non_empty(d1, d2, pre_peg, post_peg):
    # a_d_i_d_j_p_k_p_l
    # add move from peg with single disk to non empty peg
    name = "_".join(["a", d1, d2, pre_peg, post_peg])
    pre = create_obj_at_obj(d1, pre_peg) + " " + create_top_disk(d1)
    pre += " " + create_obj_at_obj(d2, post_peg) + " " + create_top_disk(d2)
    pre += " " + create_ground_disk(d1)
    add_props = create_empty_peg(post_peg) + " " + create_obj_at_obj(d1, post_peg)
    add_props += " " + create_obj_at_obj(d1, d2)
    delete_props = create_obj_at_obj(d1, pre_peg) + " " + create_top_disk(d2)
    delete_props += " " + create_ground_disk(d1)
    return (name, pre, add_props, delete_props)

def disk_to_non_empty(d1, d2, d3, pre_peg, post_peg):
    # d_i_d_j_d_k_p_l_p_r
    # add move from peg with multiple disks to non empty peg
    name = "_".join([d1, d2, d3, pre_peg, post_peg])
    pre = create_obj_at_obj(d1, pre_peg) + " " + create_top_disk(d1)
    pre += " " + create_obj_at_obj(d1, d2) + " " + create_obj_at_obj(d3, post_peg)
    pre += " " + create_top_disk(d3) + " " + create_disk_less_than_disk(d1, d2)
    pre += " " + create_disk_less_than_disk(d1, d3)
    add_props = create_obj_at_obj(d1, d3) + " " + create_obj_at_obj(d1, post_peg)
    add_props += " " + create_top_disk(d2)
    delete_props = create_top_disk(d3) + " " + create_obj_at_obj(d1, pre_peg)
    delete_props += create_obj_at_obj(d1 , d2)
    return (name, pre, add_props, delete_props)


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file
    
    # create propositions
    disk_at_peg = " ".join([create_obj_at_obj(d, p) for d in disks for p in pegs])
    disk_on_disk = " ".join([create_obj_at_obj(di, dj) for di in disks for dj in disks if di < dj])
    disk_less_than_disk = " ".join([create_disk_less_than_disk(di, dj) for di in disks for dj in disks if di < dj])
    empty_peg = " ".join([create_empty_peg(p) for p in pegs])
    top_disk = " ".join([create_top_disk(d) for d in disks])
    disk_alone = " ".join([create_ground_disk(d) for d in disks])

    domain_file.write("Propositions:\n")
    props = " ".join([disk_at_peg, disk_on_disk, empty_peg, top_disk, disk_less_than_disk, disk_alone])
    domain_file.write(props + "\n")  

    # create actions
    domain_file.write("Actions:\n")
    for peg_0, peg_1 in combinations(pegs, 2):
        for pre_peg, post_peg in [(peg_0, peg_1), (peg_1, peg_0)]:
 
            # a_d_i_p_j_p_k
            for disk in disks:
                move = alone_to_empty(disk, pre_peg, post_peg)
                write_move(domain_file, move)

            for di, dj in combinations(disks, 2):
                if di >= dj:
                    continue

                # d_i_d_j_p_k_e_p_l
                move = disk_to_empty(di, dj, pre_peg, post_peg)
                write_move(domain_file, move)

                # a_d_i_d_j_p_k_p_l
                move = alone_to_non_empty(di, dj, pre_peg, post_peg)
                write_move(domain_file, move)

            for di, dj, dk in combinations(disks, 3):
                if di >= dj or di >= dk:
                    continue

                # d_i_d_j_d_k_p_l_p_r
                move = disk_to_non_empty(di, dj, dk, pre_peg, post_peg)
                write_move(domain_file, move)

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    initial_str = write_all_disks_on_peg(0, n_, m_)
    # add disk k > disk [k]
    disk_less_than_disk = " ".join([create_disk_less_than_disk(di, dj) for di in disks for dj in disks if di < dj])
    initial_str += " " + disk_less_than_disk

    goal_str = write_all_disks_on_peg(m_ - 1, n_, m_)

    problem_file.write(initial_str + "\n" + goal_str)
    problem_file.close()


def write_all_disks_on_peg(final_peg, n_, m_):
    to_write = "Initial state:"

    if final_peg == (m_ - 1):
        to_write = "Goal state:"

    # all disks are on peg final_peg:
    to_write += ''.join([" d_%s_p_%s" % (i, final_peg) for i in list(range(n_))])

    # all pegs beside final_peg are empty:
    ran = list(range(m_))
    ran.remove(final_peg)
    to_write += ''.join(" e_p_%s" % i for i in ran)

    # disk 0 on top (is free):
    to_write += " f_d_0"

    # disk k-1 is on to of disk k:
    to_write += ''.join([" d_%s_d_%s" % (i, j) for (i, j) in
                     np.stack((np.array(range(n_ - 1)), np.array(range(1, n_))), axis=-1)])

    # disk n - 1 is on the ground:
    to_write += " g_d_" + str(n_ - 1)

    return to_write


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
