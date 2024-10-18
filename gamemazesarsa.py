# -*- coding: utf-8 -*-
"""GameMazeSarsa.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1v4ODi08wCAiy0Ap2yFfF7LgUlZ5xzf97
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
from IPython.display import clear_output
import csv

# Khởi tạo mê cung (0 = đường đi, 1 = tường, 2 = đích)
maze = np.array([
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 0, 1, 0, 0, 0, 2]
])

# Vị trí ban đầu của agent
agent_pos = [0, 0]

# Các hướng di chuyển [lên, xuống, trái, phải]
actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

# SARSA
Q_table = np.zeros((maze.shape[0], maze.shape[1], 4))
alpha = 0.1
gamma = 0.9
epsilon = 0.1

# Hàm chọn hành động
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.randint(0, 4)
    else:
        return np.argmax(Q_table[state[0], state[1]])

# Hàm kiểm tra nếu một vị trí là hợp lệ
def valid_move(pos):
    if 0 <= pos[0] < maze.shape[0] and 0 <= pos[1] < maze.shape[1]:
        return maze[pos[0], pos[1]] != 1
    return False

# Hàm kiểm tra nếu agent bị kẹt (đường cụt)
def is_dead_end(pos):
    dead_end = True
    for action in actions:
        new_pos = [pos[0] + action[0], pos[1] + action[1]]
        if valid_move(new_pos):
            dead_end = False
            break
    return dead_end

# Tính phần thưởng
def get_reward(pos):
    if maze[pos[0], pos[1]] == 2:
        return 100  # Đạt đích
    elif is_dead_end(pos):
        return -10  # Đường cụt
    else:
        return -0.1  # Phần thưởng âm cho mỗi bước đi

# Cập nhật Q-values theo SARSA
def update_q(state, action, reward, next_state, next_action):
    current_q = Q_table[state[0], state[1], action]
    next_q = Q_table[next_state[0], next_state[1], next_action]
    new_q = (1 - alpha) * current_q + alpha * (reward + gamma * next_q)
    Q_table[state[0], state[1], action] = new_q

# Vẽ mê cung và agent
def draw_maze(agent_pos):
    clear_output(wait=True)
    fig, ax = plt.subplots(figsize=(5, 5))

    # Vẽ lưới
    ax.set_xticks(np.arange(-.5, maze.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-.5, maze.shape[0], 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

    # Vẽ tường và đích
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 1:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True, color='black'))
            elif maze[i, j] == 2:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=True, color='green'))

    # Vẽ agent
    agent_circle = Circle((agent_pos[1], agent_pos[0]), 0.3, color='blue')
    ax.add_patch(agent_circle)

    # Ẩn trục x, y
    ax.axis('off')

    # Cài đặt giới hạn và hiển thị
    plt.xlim([-0.5, maze.shape[1] - 0.5])
    plt.ylim([maze.shape[0] - 0.5, -0.5])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Hàm lưu kết quả sau mỗi epoch vào file CSV
def save_results_to_csv(epoch, total_reward, steps, filename='training_results_sarsa.csv'):
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Epoch", "Total Reward"])
        writer.writerow([epoch + 1, total_reward])

# Hàm demo quá trình di chuyển của agent với Q-table đã được huấn luyện
def demo_best_agent_Sarsa(Q_table, delay=0.1):
    agent_pos = [0, 0]  # Đặt lại vị trí ban đầu

    while maze[agent_pos[0], agent_pos[1]] != 2:  # Tiếp tục cho đến khi đến đích
        draw_maze(agent_pos)
        action = np.argmax(Q_table[agent_pos[0], agent_pos[1]])  # Chọn hành động tốt nhất từ Q-table
        new_pos = [agent_pos[0] + actions[action][0], agent_pos[1] + actions[action][1]]

        if valid_move(new_pos):
            agent_pos = new_pos
            time.sleep(delay)  # Thêm độ trễ để quan sát quá trình di chuyển

    draw_maze(agent_pos)  # Vẽ lần cuối khi đã đến đích
    print("Agent đã đến đích!")

# Mô phỏng quá trình di chuyển của agent theo SARSA
def simulate_agent_sarsa(epochs=2000, delay=0.0001, save_filename='training_results_sarsa.csv'):
    global agent_pos
    rewards_per_epoch = []  # Danh sách để lưu tổng phần thưởng mỗi epoch
    step = 0

    for epoch in range(epochs):
        agent_pos = [0, 0]  # Đặt lại vị trí ban đầu
        total_reward = 0
        steps = 0


        while maze[agent_pos[0], agent_pos[1]] != 2:
            action = choose_action(agent_pos)
            new_pos = [agent_pos[0] + actions[action][0], agent_pos[1] + actions[action][1]]

            if valid_move(new_pos):
                reward = get_reward(new_pos)
                next_action = choose_action(new_pos)
                update_q(agent_pos, action, reward, new_pos, next_action)
                agent_pos = new_pos
                action = next_action
                total_reward += reward
                steps += 1

                draw_maze(agent_pos)
                time.sleep(delay)

        rewards_per_epoch.append(total_reward)
        print(f'Epoch {epoch + 1}: Total Reward: {total_reward}, Steps: {steps}')
        save_results_to_csv(epoch, total_reward, steps, save_filename)

    # Vẽ đồ thị tổng phần thưởng theo từng epoch
    plt.figure(figsize=(10, 4))
    plt.plot(rewards_per_epoch, label="Total Reward per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Total Reward")
    plt.title("Training Progress - Total Reward per Epoch (SARSA)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return rewards_per_epoch

# Huấn luyện agent sử dụng SARSA
training_results_sarsa = simulate_agent_sarsa()
print("Training results SARSA:", training_results_sarsa)

# Gọi hàm demo sau khi quá trình huấn luyện hoàn tất
demo_best_agent_Sarsa(Q_table)