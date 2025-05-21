#include <iostream>
#include <vector>
#include <algorithm>
#include <queue>
#include "json.hpp"  

using json = nlohmann::json;
using namespace std;

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int priority; // Lower value = higher priority
    int waiting_time;
    int turnaround_time;
    int completion_time;
};

int main() {
    json input;
    cin >> input;

    vector<Process> processes;
    for (auto& p : input["processes"]) {
        processes.push_back({
            p["pid"], p["arrival_time"], p["burst_time"], p["priority"], 0, 0, 0
        });
    }

    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival_time < b.arrival_time;
    });

    auto cmp = [](const Process& a, const Process& b) {
        return a.priority > b.priority;
    };
    priority_queue<Process, vector<Process>, decltype(cmp)> ready_queue(cmp);

    int current_time = 0;
    size_t index = 0;
    vector<Process> result;

    while (index < processes.size() || !ready_queue.empty()) {
        while (index < processes.size() && processes[index].arrival_time <= current_time) {
            ready_queue.push(processes[index]);
            index++;
        }

        if (!ready_queue.empty()) {
            auto p = ready_queue.top();
            ready_queue.pop();

            p.waiting_time = current_time - p.arrival_time;
            p.completion_time = current_time + p.burst_time;
            p.turnaround_time = p.completion_time - p.arrival_time;
            
            current_time = p.completion_time;
            result.push_back(p);
        } else {
            current_time = processes[index].arrival_time;
        }
    }

    json output;
    output["algorithm"] = "priority";
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