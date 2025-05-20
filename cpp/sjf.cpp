#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Process {
    int id;
    int arrivalTime;
    int burstTime;
    int remainingTime;
    int finishTime;
};

struct CompareRemainingTime {
    bool operator()(Process* a, Process* b) {
        return a->remainingTime > b->remainingTime;
    }
};

void runSJF_Preemptive(vector<Process>& processes) {
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrivalTime < b.arrivalTime;
    });

    priority_queue<Process*, vector<Process*>, CompareRemainingTime> readyQueue;
    int currentTime = 0, completed = 0, index = 0;

    cout << "\nGantt Chart:\n";
    cout << "--------------------------------------------------\n";

    while (completed < processes.size()) {
        while (index < processes.size() && processes[index].arrivalTime <= currentTime) {
            readyQueue.push(&processes[index]);
            index++;
        }

        if (!readyQueue.empty()) {
            Process* current = readyQueue.top();
            readyQueue.pop();
            cout << "| P" << current->id << " (" << currentTime << ") ";
            current->remainingTime--;
            currentTime++;

            if (current->remainingTime == 0) {
                current->finishTime = currentTime;
                completed++;
            } else {
                readyQueue.push(current);
            }
        } else {
            cout << "| IDLE (" << currentTime << ") ";
            currentTime++;
        }
    }
    cout << "|\n--------------------------------------------------\n";

    // Metrics table (same as FCFS)
    // ...
    float totalWaiting = 0, totalTurnaround = 0;
    cout << "\nProcess\tArrival\tBurst\tFinish\tWaiting\tTurnaround\n";
    cout << "--------------------------------------------------\n";
    for (const auto& p : processes) {
        int waiting = p.finishTime - p.arrivalTime - p.burstTime;
        int turnaround = p.finishTime - p.arrivalTime;
        totalWaiting += waiting;
        totalTurnaround += turnaround;
        cout << "P" << p.id << "\t" << p.arrivalTime << "\t" << p.burstTime << "\t" 
             << p.finishTime << "\t" << waiting << "\t" << turnaround << endl;
    }

    cout << "\nAverage Waiting Time: " << totalWaiting / processes.size() << endl;
    cout << "Average Turnaround Time: " << totalTurnaround / processes.size() << endl;
}

int main() {
    // Same input as FCFS
    // ...
    int n;
    cout << "Enter number of processes: ";
    cin >> n;

    vector<Process> processes(n);
    for (int i = 0; i < n; i++) {
        processes[i].id = i + 1;
        cout << "Enter Arrival Time for P" << i+1 << ": ";
        cin >> processes[i].arrivalTime;
        cout << "Enter Burst Time for P" << i+1 << ": ";
        cin >> processes[i].burstTime;
    }

    runSJF_Preemptive(processes);
    return 0;
}