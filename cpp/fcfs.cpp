#include <iostream>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Process {
    int id;
    int arrivalTime;
    int burstTime;
    int finishTime;
};

void runFCFS(vector<Process>& processes) {
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrivalTime < b.arrivalTime;
    });

    int currentTime = 0;
    cout << "\nGantt Chart:\n";
    cout << "--------------------------------------------------\n";

    for (auto& p : processes) {
        if (currentTime < p.arrivalTime) {
            cout << "| IDLE (" << currentTime << "-" << p.arrivalTime << ") ";
            currentTime = p.arrivalTime;
        }
        cout << "| P" << p.id << " (" << currentTime << "-" << currentTime + p.burstTime << ") ";
        p.finishTime = currentTime + p.burstTime;
        currentTime += p.burstTime;
    }
    cout << "|\n--------------------------------------------------\n";

    // Calculate metrics
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

    runFCFS(processes);
    return 0;
}