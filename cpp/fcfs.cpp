#include <iostream>
#include <vector>
#include <algorithm>
#include "json.hpp"  

using json = nlohmann::json;
using namespace std;

struct Process {
    int pid;
    int arrival_time;
    int burst_time;
    int priority;
    int waiting_time;
    int turnaround_time;
    int completion_time;
};

int main() {
    // Reading JSON input
    json input;
    cin >> input;

    // Parsing processes
    vector<Process> processes;
    for (auto& p : input["processes"]) {
        processes.push_back({
            p["pid"], p["arrival_time"], p["burst_time"], p["priority"], 0, 0, 0
        });
    }

    // Sorting by arrival time (FCFS)
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrival_time < b.arrival_time;
    });

    // Calculating times
    int current_time = 0;
    for (auto& p : processes) {
        if (current_time < p.arrival_time) {
            current_time = p.arrival_time;
        }
        
        p.waiting_time = current_time - p.arrival_time;
        p.completion_time = current_time + p.burst_time;
        p.turnaround_time = p.completion_time - p.arrival_time;
        
        current_time = p.completion_time;
    }

    // Preparing output
    json output;
    output["algorithm"] = "fcfs";
    output["processes"] = json::array();
    
    for (const auto& p : processes) {
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