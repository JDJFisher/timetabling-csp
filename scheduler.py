import module
import tutor
import ReaderWriter
import timetable
import random
import math

class Scheduler:
    def __init__(self,tutorList, moduleList):
        self.tutorList = tutorList
        self.moduleList = moduleList

    #Using the tutorlist and modulelist, create a timetable of 5 slots for each of the 5 work days of the week.
    #The slots are labelled 1-5, and so when creating the timetable, they can be assigned as such:
    #	timetableObj.addSession("Monday", 1, Smith, CS101, "module")
    #This line will set the session slot '1' on Monday to the module CS101, taught by tutor Smith.
    #Note here that Smith is a tutor object and CS101 is a module object, they are not strings.
    #The day (1st argument) can be assigned the following values: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    #The slot (2nd argument) can be assigned the following values: 1, 2, 3, 4, 5 in task 1 and 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 in tasks 2 and 3.
    #Tutor (3rd argument) and module (4th argument) can be assigned any value, but if the tutor or module is not in the original lists,
    #	your solution will be marked incorrectly.
    #The final, 5th argument, is the session type. For task 1, all sessions should be "module". For task 2 and 3, you should assign either "module" or "lab" as the session type.
    #Every module needs one "module" and one "lab" session type.

    #moduleList is a list of Module objects. A Module object, 'm' has the following attributes:
    # m.name  - the name of the module
    # m.topics - a list of strings, describing the topics that module covers e.g. ["Robotics", "Databases"]

    #tutorList is a list of Tutor objects. A Tutor object, 't', has the following attributes:
    # t.name - the name of the tutor
    # t.expertise - a list of strings, describing the expertise of the tutor.

    #For Task 1:
    #Keep in mind that a tutor can only teach a module if the module's topics are a subset of the tutor's expertise.
    #Furthermore, a tutor can only teach one module a day, and a maximum of two modules over the course of the week.
    #There will always be 25 modules, one for each slot in the week, but the number of tutors will vary.
    #In some problems, modules will cover 2 topics and in others, 3.
    #A tutor will have between 3-8 different expertise fields.

    #For Task 2 and 3:
    #A tutor can only teach a lab if they have at least one expertise that matches the topics of the lab
    #Tutors can only manage a 'credit' load of 4, where modules are worth 2 and labs are worth 1.
    #A tutor can not teach more than 2 credits per day.

    #You should not use any other methods and/or properties from the classes, these five calls are the only methods you should need.
    #Furthermore, you should not import anything else beyond what has been imported above.

    #This method should return a timetable object with a schedule that is legal according to all constraints of task 1.
    def createSchedule(self):
        # Create empty timetable
        timetableObj = timetable.Timetable(1)

        # Use backtracking algorithm to recursively schedule each module with
        # a valid tutor to a given day
        schedule = self.backtrackingSearch()

        # Look-up list for day strings
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Populate the timetable object with all of the sessions in the schedule
        for day, sessions in enumerate(schedule):
            for slot, (module, tutor) in enumerate(sessions):
                # Record the session in the timetable with the approriate day and session number
                timetableObj.addSession(days[day], slot + 1, tutor, module, "module")

        # Return timetable
        return timetableObj

    def backtrackingSearch(self):
        # Create an empty schedule
        schedule = [list() for day in range(5)]

        u_modules = self.moduleList.copy()
        # Form a list containing each tutor twice
        available_tutors = self.tutorList * 2

        # Begin recursively assigning the modules and tutors to the schedule
        self.recursiveBacktracking(schedule, u_modules, available_tutors)

        return schedule

    def recursiveBacktracking(self, schedule, u_modules, available_tutors):
        # All modules have sucessfully been assigned
        if not u_modules: return True

        # Select the next module to be assigned
        module = u_modules[0]

        for day in schedule:
            for tutor in available_tutors:
                # Check whether scheduling the module & tutor together on
                # the given day is legal
                if (self.consistantSession(day, module, tutor)):
                    # Schedule the module and tutor to the given day
                    day.append((module, tutor))
                    u_modules.remove(module)
                    available_tutors.remove(tutor)

                    # After sucessfully adding a session to the schedule,
                    # attempt to recursively assign the next session
                    if self.recursiveBacktracking(schedule, u_modules, available_tutors):
                        return True

                    # Revert previous assignment
                    day.pop()
                    u_modules.append(module)
                    available_tutors.append(tutor)


        # Given the current schedule, the selected module could not be assinged
        # with any of the tutors to any of the days. return False to inicate
        # failure and to start backtracking
        return False

    def consistantSession(self, day, module, tutor):
        full = len(day) == 5
        busy = any(t == tutor for _,t in day)
        able = all(subject in tutor.expertise for subject in module.topics)

        return able and not busy and not full




















    #Now, we have introduced lab sessions. Each day now has ten sessions, and there is a lab session as well as a module session.
    #All module and lab sessions must be assigned to a slot, and each module and lab session require a tutor.
    #The tutor does not need to be the same for the module and lab session.
    #A tutor can teach a lab session if their expertise includes at least one topic covered by the module.
    #We are now concerned with 'credits'. A tutor can teach a maximum of 4 credits. Lab sessions are 1 credit, module sessiosn are 2 credits.
    #A tutor cannot teach more than 2 credits a day.
    def createLabSchedule(self):
        # Create empty timetable
        timetableObj = timetable.Timetable(2)

        # Use backtracking algorithm to recursively schedule each module and
        # lab with a valid tutor to a given day
        schedule = self.backtrackingSearchLab()

        # Look-up list for day strings
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Populate the timetable object with all of the sessions in the schedule
        for day, sessions in enumerate(schedule):
            for slot, (module, tutor, type) in enumerate(sessions):
                # Record the session in the timetable with the approriate day and session number
                timetableObj.addSession(days[day], slot + 1, tutor, module, type)

        return timetableObj

    def backtrackingSearchLab(self):
        schedule = [list() for d in range(5)]
        u_modules = self.moduleList.copy()
        u_labs = self.moduleList.copy()
        tutor_credits = dict.fromkeys(self.tutorList, 4)

        self.recursiveBacktrackingLab(schedule, u_modules, u_labs, tutor_credits)

        return schedule

    def recursiveBacktrackingLab(self, schedule, u_modules, u_labs, tutor_credits):
        # If there are unassigned modules, try schedule them with a tutor
        # before the labs
        if u_modules:
            # Select the next module to be assigned
            module = u_modules[0]

            for day in schedule:
                for tutor, credits in tutor_credits.items():
                    # Check whether scheduling the module & tutor together on
                    # the given day is legal
                    if self.consistentModule(day, module, tutor, credits):

                        # Add the module session to the day's sessions
                        day.append((module, tutor, "module"))
                        u_modules.remove(module)
                        tutor_credits[tutor] = credits-2

                        # After sucessfully adding a session to the schedule,
                        # attempt to recursively assign the next session
                        if self.recursiveBacktrackingLab(schedule, u_modules, u_labs, tutor_credits):
                            return True

                        # Revert previous assignment
                        day.pop()
                        u_modules.append(module)
                        tutor_credits[tutor] = credits

        # If all modules have been sucessfully scheduled, begin assigning the labs
        elif u_labs:
            # Select the next lab to be assigned
            lab = u_labs[0]

            for day in schedule:
                for tutor, credits in tutor_credits.items():
                    # Check whether scheduling the lab & tutor together on
                    # the given day is legal
                    if self.consistentLab(day, lab, tutor, credits):

                        # Add the lab session to the day's sessions
                        day.append((lab, tutor, "lab"))
                        u_labs.remove(lab)
                        tutor_credits[tutor] = credits-1

                        # After sucessfully adding a session to the schedule,
                        # attempt to recursively assign the next session
                        if self.recursiveBacktrackingLab(schedule, u_modules, u_labs, tutor_credits):
                            return True

                        # Revert previous assignment
                        day.pop()
                        u_labs.append(lab)
                        tutor_credits[tutor] = credits
        else:
            # All seessions have been sucessfully scheduled, return True to
            # signify a complete legal schedule
            return True

        # Given the current schedule, the selected sessions could not be assinged
        # with any of the tutors to any of the days. return False to inicate
        # failure and to start backtracking
        return False

    def consistentModule(self, day, module, tutor, credits):
        enough_credits = credits >= 2
        full = len(day) == 10
        able = all(subject in tutor.expertise for subject in module.topics)
        busy = any(t == tutor for _,t,_ in day)

        return enough_credits and able and not busy and not full

    def consistentLab(self, day, module, tutor, credits):
        enough_credits = credits >= 1
        full = len(day) == 10
        able = any(subject in tutor.expertise for subject in module.topics)
        busy = sum(2 if type == 'module' else 1 for _,t,type in day if t == tutor) > 1

        return enough_credits and able and not busy and not full















    #It costs £500 to hire a tutor for a single module.
    #If we hire a tutor to teach a 2nd module, it only costs £300. (meaning 2 modules cost £800 compared to £1000)
    #If those two modules are taught on consecutive days, the second module only costs £100. (meaning 2 modules cost £600 compared to £1000)

    #It costs £250 to hire a tutor for a lab session, and then £50 less for each extra lab session (£200, £150 and £100)
    #If a lab occurs on the same day as anything else a tutor teaches, then its cost is halved.

    #Using this method, return a timetable object that produces a schedule that is close, or equal, to the optimal solution.
    #You are not expected to always find the optimal solution, but you should be as close as possible.
    #You should consider the lecture material, particular the discussions on heuristics, and how you might develop a heuristic to help you here.
    def createMinCostSchedule(self):
        # Create empty timetable
        timetableObj = timetable.Timetable(3)

        # Asign a tutor to all 50 lab and module sessions using A* search algorithm
        tutor_modules, tutor_labs = self.findPairings()

        # Arrange all of the previously determined sessions into a legal
        # timetable schedule while minimising cost
        schedule = Scheduler.tableSessions(tutor_modules, tutor_labs)

        # Look-up list for day strings
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        # Populate the timetable object with all of the sessions in the schedule
        for day, sessions in enumerate(schedule):
            for slot, (module, tutor, type) in enumerate(sessions):
                # Record the session in the timetable with the approriate day and session number
                timetableObj.addSession(days[day], slot + 1, tutor, module, type)

        return timetableObj

    def findPairings(self):
        end_state = None

        # In the rare event that all goal nodes are culled, repeat the search
        while end_state is None:

            # Initialise the dictionaries such that all tutors intially teach no sessions
            tutor_modules = {tutor : set() for tutor in self.tutorList}
            tutor_labs =    {tutor : set() for tutor in self.tutorList}

            # Create a list of session tuples
            u_sessions = [(l, "lab") for l in self.moduleList] + [(m, "module") for m in self.moduleList]

            # Form the start state and begin the search for tutor session pairings
            start_state = Scheduler.State(u_sessions, tutor_modules, tutor_labs)
            end_state = Scheduler.a_star_search(start_state)

        return end_state.tutor_modules, end_state.tutor_labs

    def a_star_search(start_state):
        # Initialise the open list with the search start state
        open_list = [start_state]

        # While there are unexplored states on the frontier, continue to search
        while open_list:
            # Select the optimal state to seach next by removing the state with the
            # minimum f score from the openlist
            state = Scheduler.PriorityQ.removeMin(open_list)

            # Generate all possible successors of the selected state
            successors = state.generateSuccessors()

            # Limit the branching factor to 2 by randomly culling successors
            random.shuffle(successors)
            successors = successors[:2]

            for successor in successors:
                # If a goal state has been created end the search
                if successor.is_goal(): return successor

                # Determine the new state's f score and place it in the open list
                # according to the score
                successor.calc_f()
                Scheduler.PriorityQ.insert(open_list, successor)

        # Fully exploring the start state yielded no descendant goal states. Failure.
        return None

    def tableSessions(tutor_modules, tutor_labs):
        # Create an empty list for each day of the week that the sessions can be
        # allocated to
        schedule = [[] for i in range(5)]

        # Iterate over all tutors that have been allocated exactly 2 modules and
        # add their modules to the schedule on consecutive days
        for tutor, modules in tutor_modules.items():
            if len(modules) == 2:
                # Select either day group 0 (Monday & Tuesday) or 3 (Thursday &
                # Friday) favouring the group with less module pairs assinged
                day = 3 if len(schedule[3]) < len(schedule[0]) else 0

                # Add the first module to the first day in the selected group
                schedule[day  ].append((modules.pop(), tutor, "module"))
                # Add the other module to the following day's from thr group
                schedule[day+1].append((modules.pop(), tutor, "module"))

        # Iterate over all tutors that have been allocated at least 2 lab sessions
        # and place lab pairings in consecutive timeslots on any day with 2 slots
        for tutor, labs in tutor_labs.items():
            for day in schedule:
                if len(labs) >= 2 and len(day) <= 8:
                    day.append((labs.pop(), tutor, "lab"))
                    day.append((labs.pop(), tutor, "lab"))

        # Collect all remaining session tutor pairings that have not been assinged
        u_modules = [(m.pop(), t, "module") for t, m in tutor_modules.items() if m]
        u_labs    = [(l.pop(), t, "lab"   ) for t, l in tutor_labs.items()    if l]

        # After strategically placing the discounted sessions pairs, place the
        # remaining unassigned single sessions to complete the schedule
        Scheduler.fillGaps(schedule, u_modules + u_labs)

        return schedule

    def fillGaps(schedule, u_sessions):
        # While there are unassigned sessions, add each session to any day where
        # there is both space and the addition is legal
        while u_sessions:
            session, tutor, type = u_sesh = u_sessions.pop()
            added = False

            for day in schedule:
                if not added and len(day) < 10 and not any(t == tutor for _,t,_ in day):
                    # Session assigned
                    day.append(u_sesh)
                    added = True

            # In the isolated case where a tutor has been assigned a single session
            # of both types, there may be no remaining empty legal slots after
            # assigning one of the sessions.
            if not added:
                # Choose random legal slot from the schedule
                day = random.choice([d for d in schedule if not any(t == tutor for _,t,_ in d)])
                scheduled_sesh = random.choice(day)

                # Swap in the blocked session for the session already in the slot
                day.remove(scheduled_sesh)
                day.append(u_sesh)
                u_sessions.append(scheduled_sesh)

    class PriorityQ:
        # Pop and return the smallest element from the sorted queue
        def removeMin(q):
            return q.pop()

        # Insert item x in order into a sorted PQ q
        def insert(q, x):
            lo = 0
            hi = len(q)

            # Apply binary search to find ordered insersion index
            while lo < hi:
                mid = (lo+hi) // 2

                if x > q[mid]:
                    hi = mid
                else:
                    lo = mid+1

            # Insert the item at the determined index
            q.insert(lo, x)

    class State:
        # State constructor
        def __init__(self, u_sessions, tutor_modules, tutor_labs):
            self.u_sessions = u_sessions.copy()
            self.tutor_modules = {t : m.copy() for t, m in tutor_modules.items()}
            self.tutor_labs =    {t : l.copy() for t, l in tutor_labs.items()}
            self.f = 0

        # The state is a goal iff all sessions have been allocated a legal tutor
        def is_goal(self):
            return not self.u_sessions

        def generateSuccessors(self):
            # Create a new list for any potential successor states
            successors = []

            # Choose the next session that will be assinged in all successors
            session, type = self.u_sessions.pop()

            for tutor in self.tutor_modules:
                # Determine how many remaining credits the tutor has
                credits = 4 - 2 * len(self.tutor_modules[tutor]) - len(self.tutor_labs[tutor])

                # Check whether the tutor is able to teach the session depending on the type
                if type == "module":
                    able = credits >= 2 and all(subject in tutor.expertise for subject in session.topics)
                else:
                    able = credits >= 1 and any(subject in tutor.expertise for subject in session.topics)

                if able:
                    # Generate a copy successor state
                    successor = Scheduler.State(self.u_sessions, self.tutor_modules, self.tutor_labs)

                    # Add the session to the tutors taught sessions
                    tutor_sessions = successor.tutor_modules if type == "module" else successor.tutor_labs
                    tutor_sessions[tutor].add(session)

                    # Add the new successor state
                    successors.append(successor)

            return successors

        # Less than operator overload for States
        def __lt__(self, other):
            # Order states by their f scores
            return self.f < other.f

        # Calculates the f score of the state to determine its position in the open list
        def calc_f(self):
            # Calculate the f score as the sum of the g & h scores
            self.f = self.calc_g() + self.calc_h()

        def calc_g(self):
            g = 0

            # Iterate over all the sets of modules that have been assinged to tutors
            # and increment the g score by the cost of the modules assuming that the
            # modules will be timetabled consecutively to achieve the discout
            for tutor, modules in self.tutor_modules.items():
                if len(modules) == 1:
                    g += 500
                elif len(modules) == 2:
                    g += 600 # 500 + 100

            # Iterate over all the sets of labs that have been assinged to tutors
            # and increment the g score by the discounted cost of the labs assuming
            # that the labs will be paired up when timetabled
            for tutor, labs in self.tutor_labs.items():
                if len(labs) == 1:
                    g += 250
                elif len(labs) == 2:
                    g += 225 # (250 + 200) / 2
                elif len(labs) == 3:
                    g += 375 # (250 + 200) / 2 + 150
                elif len(labs) == 4:
                    g += 350 # (250 + 200) / 2 + (150 + 100) / 2

            return g

        def calc_h(self):
            h = 0

            # Seperate the unassigned sessions into unassigned modules and labs
            u_modules = [s for s,type in self.u_sessions if type == "module"]
            u_labs = [s for s,type in self.u_sessions if type == "lab"]

            # Create dictionaries that track the estimated number of modules and
            # labs the tutors will be allocated after assigning remaining
            # sessions. Initialise with the assinged number of labs and modules
            tutor_p_mod_count = {t : len(ms) for t, ms in self.tutor_modules.items()}
            tutor_p_lab_count = {t : len(ls) for t, ls in self.tutor_labs.items()}

            for module in u_modules:
                # Initialise an empty list for tutors that could potential teach the module
                possible_tutors = []

                for tutor in tutor_p_mod_count:
                    credits = 4 - tutor_p_mod_count[tutor] * 2 - tutor_p_lab_count[tutor]

                    if credits >= 2 and all(subject in tutor.expertise for subject in module.topics):
                        possible_tutors.append(tutor)

                if possible_tutors:
                    tutor = max(possible_tutors, key=lambda t : tutor_p_mod_count[t])

                    count = tutor_p_mod_count[tutor]

                    if count == 0:
                        h += 500
                    else:
                        h += 100

                    tutor_p_mod_count[tutor] = count+1

            for lab in u_labs:
                possible_tutors = []

                for tutor in tutor_p_lab_count:
                    credits = 4 - tutor_p_mod_count[tutor] * 2 - tutor_p_lab_count[tutor]

                    if credits >= 1 and any(subject in tutor.expertise for subject in lab.topics):
                        possible_tutors.append(tutor)

                if possible_tutors:
                    tutor = max(possible_tutors, key=lambda t : tutor_p_lab_count[t])

                    count = tutor_p_lab_count[tutor]

                    if count == 0:
                        h += 250
                    elif count == 1:
                        h -= 25
                    elif count == 2:
                        h += 150
                    else:
                        h -= 25

                    # increment the tutors estimated lab count
                    tutor_p_lab_count[tutor] = count+1

            return h

        def searcho(u_sessions, tutor_modules, tutor_labs):
            if not u_sessions:
                return 0

            session, type = u_sessions[0]



            for tutor in tutor_modules:
                credits = 4 - tutor_modules[tutor] * 2 - tutor_labs[tutor]

                if type == "module":
                    legal = credits >= 2 and all(subject in tutor.expertise for subject in session.topics)
                else:
                    legal = credits >= 1 and all(subject in tutor.expertise for subject in session.topics)


                    moduleTutors[module] = tutor
                    tutorCreds[tutor] = credits-2
                    unassignedModules.remove(module)

                    if pair(unassignedModules, unassignedLabs, tutorCreds, moduleTutors, labTutors):
                        return True

                    moduleTutors[module] = None
                    tutorCreds[tutor] = credits
                    unassignedModules.append(module)
