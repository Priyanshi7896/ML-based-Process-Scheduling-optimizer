#include <iostream>
#include <vector>
#include <algorithm> // for sort()

using namespace std;

struct Process {
    int id;
    int arrivalTime;
    int burstTime;
};

// Function to compute FCFS scheduling
void runFCFS(vector<Process>& processes) {
    // Sort processes by arrival time (FCFS order)
    sort(processes.begin(), processes.end(), [](const Process& a, const Process& b) {
        return a.arrivalTime < b.arrivalTime;
    });

    int currentTime = 0;
    float totalWaitingTime = 0;
    float totalTurnaroundTime = 0;

    cout << "\nGantt Chart:\n";
    cout << "--------------------------------------------------\n";

    for (const auto& p : processes) {
        if (currentTime < p.arrivalTime) {
            currentTime = p.arrivalTime; // Handle idle time
        }

        int waitingTime = currentTime - p.arrivalTime;
        int turnaroundTime = waitingTime + p.burstTime;

        // Update totals
        totalWaitingTime += waitingTime;
        totalTurnaroundTime += turnaroundTime;

        // Print process execution
        cout << "| P" << p.id << " (" << currentTime << "-" << currentTime + p.burstTime << ") ";
        currentTime += p.burstTime;
    }

    cout << "|\n--------------------------------------------------\n";

    // Calculate averages
    float avgWaitingTime = totalWaitingTime / processes.size();
    float avgTurnaroundTime = totalTurnaroundTime / processes.size();

    cout << "\nAverage Waiting Time: " << avgWaitingTime << endl;
    cout << "Average Turnaround Time: " << avgTurnaroundTime << endl;
}

int main() {
    int n;
    cout << "Enter number of processes: ";
    cin >> n;

    vector<Process> processes(n);

    // Input process details
    for (int i = 0; i < n; i++) {
        processes[i].id = i + 1;
        cout << "Enter Arrival Time for P" << i+1 << ": ";
        cin >> processes[i].arrivalTime;
        cout << "Enter Burst Time for P" << i+1 << ": ";
        cin >> processes[i].burstTime;
    }

    runFCFS(processes); // Execute FCFS
    return 0;
}