#include <iostream>
#include <vector>
#include <queue>
#include "json.hpp"  // Instead of #include <nlohmann/json.hpp>

using json = nlohmann::json;
using namespace std;

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int priority;
    int remaining_time;
    int waiting_time;
    int turnaround_time;
    int completion_time;
};

int main() {
    json input;
    cin >> input;

    int time_quantum = input["time_quantum"];
    vector<Process> processes;
    for (auto& p : input["processes"]) {
        processes.push_back({
            p["pid"], p["arrival_time"], p["burst_time"], p["priority"], 
            p["burst_time"], 0, 0, 0
        });
    }

    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival_time < b.arrival_time;
    });

    queue<Process*> ready_queue;
    vector<Process> result;
    int current_time = 0;
    size_t index = 0;

    while (index < processes.size() || !ready_queue.empty()) {
        while (index < processes.size() && processes[index].arrival_time <= current_time) {
            ready_queue.push(&processes[index]);
            index++;
        }

        if (!ready_queue.empty()) {
            auto p = ready_queue.front();
            ready_queue.pop();

            int execution_time = min(time_quantum, p->remaining_time);
            p->remaining_time -= execution_time;
            current_time += execution_time;

            if (p->remaining_time == 0) {
                p->completion_time = current_time;
                p->turnaround_time = p->completion_time - p->arrival_time;
                p->waiting_time = p->turnaround_time - p->burst_time;
                result.push_back(*p);
            } else {
                while (index < processes.size() && processes[index].arrival_time <= current_time) {
                    ready_queue.push(&processes[index]);
                    index++;
                }
                ready_queue.push(p);
            }
        } else {
            current_time = processes[index].arrival_time;
        }
    }

    json output;
    output["algorithm"] = "rr";
    output["time_quantum"] = time_quantum;
    output["processes"] = json::array();
    
    for (const auto& p : result) {
        output["processes"].push_back({
            {"pid", p.pid},
            {"waiting_time", p.waiting_time},
            {"turnaround_time", p.turnaround_time},
            {"completion_time", p.completion_time}
        });
    }

    cout << output.dump(2);
    return 0;
}