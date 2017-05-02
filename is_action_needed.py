import datetime
import random as random
from fetch_data import *

#TEST DATA
Scholastica_v_Augustine = "http://mfl.williammck.net/poll/58d3dad399f5024018fde2d8" #Poll 194
Moses_v_Raymond = "http://mfl.williammck.net/poll/58da51fa99f50262ac984606" #Poll 190
Florence_v_Henry = "http://mfl.williammck.net/poll/58d53e6499f502208e10cd97" #Poll 191

too_early = get_data(0,30,Scholastica_v_Augustine)
test_data2 = get_data(1,30,Scholastica_v_Augustine)
big_margin = get_data(8,0,Scholastica_v_Augustine)
jank_test = get_data(13,30,Scholastica_v_Augustine)


def is_action_needed(data, person):

    print #adds space to see output more clearly

    last_time = data[-1][0]

    rates1 = []
    rates2 = []

    deltavotes1 = []
    deltavotes2 = []

    deltatime = []

    for i in range(len(data) - 1):
        deltavotes1.append(data[i + 1][1] - data[i][1])
        deltavotes2.append(data[i + 1][2] - data[i][2])
        deltatime.append(data[i + 1][0] - data[i][0])

    for k in range(len(deltavotes1)):
        rates1.append(60 * (deltavotes1[k] / float(deltatime[k])))

    for k in range(len(deltavotes2)):
        secrate2 = deltavotes2[k] / float(deltatime[k])
        rates2.append(float(60) * secrate2)

    average_rate1 = sum(rates1) / float(len(rates1))
    average_rate2 = sum(rates2) / float(len(rates2))


    now = datetime.datetime.fromtimestamp(last_time)
    eleven = datetime.datetime(now.year, now.month, now.day, 23)
    min_left = int(abs(eleven - now).seconds / 60)

    vote1_estimate = data[-1][1] + min_left * float(average_rate1)
    vote2_estimate = data[-1][2] + min_left * float(average_rate2)

    final_diff = vote1_estimate - vote2_estimate
    final_dict = {'person': person}

    if min_left > 720:
        print "It is too early to determine if action is needed. There are still %s minutes left in Lent Madness today" % (min_left)
        return False
    elif vote1_estimate > vote2_estimate and person == 2:
        add = int(final_diff * 2.25) + 2
        print "We need %s votes in %s minutes" % (add, min_left)

        final_dict.update(votes=add, minutes=min_left)
        return final_dict
    elif vote1_estimate > vote2_estimate and person == 1:
        if final_diff > 2500:
            print "No action is needed, person one is projected to win by atleast 2500 votes"
            return False
        elif final_diff < 2500:
            add = int(final_diff * 1.5) + 2
            print "We need %s votes in %s minutes" % (add, min_left)

            final_dict.update(votes=add, minutes=min_left)
            return final_dict
    elif vote2_estimate > vote1_estimate and person == 1:
        add = int(abs(final_diff) * 2.25) + 2
        print "We need %s votes in %s minutes" % (add, min_left)

        final_dict.update(votes=add, minutes=min_left)
        return final_dict
    elif vote2_estimate > vote1_estimate and person == 2:
        if abs(final_diff) > 2500:
            return False
        elif abs(final_diff) < 2500:
            add = int(abs(final_diff) * 1.5) + 2
            print "We need %s votes in %s minutes" % (add, min_left)

            final_dict.update(votes=add, minutes=min_left)
            return final_dict

is_action_needed(jank_test,2)

#PYTEST
expected_response = {'person':2,'votes':7289,'minutes':561}

def test_action_not_needed():
    assert is_action_needed(too_early,1) == False
    assert is_action_needed(too_early,2) == False
    assert is_action_needed(big_margin,1) == False

def test_action_is_needed():
    assert is_action_needed(big_margin,2) != False
