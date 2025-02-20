#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <fstream>
#include <windows.h>
#include <string>
#include <ctime>  // Para pegar data e hora


std::wstring stringToWString(const std::string& str) {
    int size_needed = MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), NULL, 0);
    std::wstring wstrTo(size_needed, 0);
    MultiByteToWideChar(CP_UTF8, 0, str.c_str(), (int)str.size(), &wstrTo[0], size_needed);
    return wstrTo;
}

std::string getCurrentTimestamp() {
    std::time_t t = std::time(nullptr);
    char buffer[20];
    std::strftime(buffer, sizeof(buffer), "%y-%m-%d %H-%M", std::localtime(&t));
    return std::string(buffer);
}

void readFromSerial(const std::string& portName, std::string& outputFilePath, DWORD baudRate) {
    // Convert portName to wstring
    std::wstring wPortName = stringToWString(portName);

    // Open the serial port
    HANDLE hSerial = CreateFile(wPortName.c_str(), GENERIC_READ, 0, 0, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
    if (hSerial == INVALID_HANDLE_VALUE) {
        std::cerr << "Error opening serial port" << std::endl;
        return;
    }

    // Set the parameters for the serial port
    DCB dcbSerialParams = { 0 };
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (!GetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Error getting serial port state" << std::endl;
        CloseHandle(hSerial);
        return;
    }
    dcbSerialParams.BaudRate = baudRate;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity = NOPARITY;
    if (!SetCommState(hSerial, &dcbSerialParams)) {
        std::cerr << "Error setting serial port state" << std::endl;
        CloseHandle(hSerial);
        return;
    }

    // Set timeouts for the serial port
    COMMTIMEOUTS timeouts = { 0 };
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;
    if (!SetCommTimeouts(hSerial, &timeouts)) {
        std::cerr << "Error setting serial port timeouts" << std::endl;
        CloseHandle(hSerial);
        return;
    }

    // Buffer to store the read data
    const int bufferSize = 256;
    char buffer[bufferSize];
    DWORD bytesRead;

    // Variable to control when to start writing to the file
    bool startWriting = false;
    bool capturingFileName = true;
    bool hashtagFound = false;

    std::string newFileName;
    std::ofstream outputFile;

    // Read data from the serial port and write to the file
    while (true) {
        if (ReadFile(hSerial, buffer, bufferSize, &bytesRead, NULL)) {
            if (bytesRead > 0) {
                if (capturingFileName){
                    for (DWORD i = 0; i < bytesRead; i++) {
                        if (hashtagFound){
                            if (buffer[i] == '\t') {
                                // Tab character ends the file name capture
                                hashtagFound = false;

                                // Gerar o timestamp e adicionar ao nome do arquivo
                                std::string timestamp = getCurrentTimestamp();
                                outputFilePath = newFileName + " " + timestamp + ".txt";

                                outputFile.close();  // Close the current file if open
                                outputFile.open(outputFilePath);  // Open the new file
                                if (!outputFile.is_open()) {
                                    std::cerr << "Error opening new output file" << std::endl;
                                    CloseHandle(hSerial);
                                    return;
                                }
                                newFileName.clear();  // Clear the new file name string
                                std::cout << "New file name: " << outputFilePath << std::endl;
                                capturingFileName = false;
                            } else {
                                // Append the character to the new file name
                                newFileName += buffer[i];
                            }
                        }
                        else if (buffer[i] == '#') {
                            hashtagFound = true;
                            newFileName.clear();
                        }
                    }
                }

                // Check if we found the letter 'I' to start writing
                if (!startWriting && !capturingFileName) {
                    for (DWORD i = 0; i < bytesRead; i++) {
                        if (buffer[i] == 'I') {
                            startWriting = true;
                            break;
                        }
                    }
                }

                // Write to the file only if startWriting is true
                if (startWriting) {
                    outputFile.write(buffer, bytesRead);
                    std::cout.write(buffer, bytesRead); // Optional: print to console

                    // Check if we found the letter 'F' to stop writing
                    for (DWORD i = 0; i < bytesRead; i++) {
                        if (buffer[i] == 'F') {
                            std::cout << "\n'F' found, stopping writing and closing file." << std::endl;
                            outputFile.close();
                            CloseHandle(hSerial);
                            return; // Exit the function
                        }
                    }
                }
            }
        }
        else {
            std::cerr << "Error reading from serial port" << std::endl;
            break;
        }
    }

    // Clean up
    outputFile.close();
    CloseHandle(hSerial);
}

int main() {
    std::string serialPort = "COM8"; // Replace with your serial port
    std::string outputFilePath = "mudarNome.txt";
    DWORD baudRate = 1228800; // Baud rate

    readFromSerial(serialPort, outputFilePath, baudRate);

    return 0;
}
