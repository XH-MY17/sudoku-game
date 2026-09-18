# -*- coding: utf-8 -*-
"""
数独游戏生成与求解 / Sudoku Generator & Solver

自动从 Jupyter Notebook 导出
"""



import random
import os

class SudokuGame:
    def __init__(self, difficulty="medium"):
        self.size = 9
        self.difficulty = difficulty
        self.board = [[0] * self.size for _ in range(self.size)]
        self.original_board = [[0] * self.size for _ in range(self.size)]
        self.generate_puzzle()
    
    def generate_board(self):
        """生成一个完整的数独解"""
        def is_possible(row, col, num):
            # 检查行
            for x in range(self.size):
                if self.board[row][x] == num:
                    return False
            
            # 检查列
            for x in range(self.size):
                if self.board[x][col] == num:
                    return False
            
            # 检查3x3宫格
            start_row, start_col = 3 * (row // 3), 3 * (col // 3)
            for i in range(3):
                for j in range(3):
                    if self.board[i + start_row][j + start_col] == num:
                        return False
            return True
        
        def solve():
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_possible(i, j, num):
                                self.board[i][j] = num
                                if solve():
                                    return True
                                self.board[i][j] = 0
                        return False
            return True
        
        # 清空棋盘
        self.board = [[0] * self.size for _ in range(self.size)]
        solve()
    
    def remove_cells(self):
        """根据难度移除一定数量的数字"""
        if self.difficulty == "easy":
            remove_count = 40
        elif self.difficulty == "hard":
            remove_count = 56
        else:  # medium
            remove_count = 48
        
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(cells)
        
        for i, (row, col) in enumerate(cells):
            if i >= remove_count:
                break
            self.board[row][col] = 0
        
        # 保存原始谜题
        for i in range(self.size):
            for j in range(self.size):
                self.original_board[i][j] = self.board[i][j]
    
    def generate_puzzle(self):
        """生成数独谜题"""
        self.generate_board()
        self.remove_cells()
    
    def is_valid(self, row, col, num):
        """检查填入的数字是否符合规则"""
        if num == 0:
            return True
        
        # 检查行（排除当前列）
        for x in range(self.size):
            if x != col and self.board[row][x] == num:
                return False
        
        # 检查列（排除当前行）
        for x in range(self.size):
            if x != row and self.board[x][col] == num:
                return False
        
        # 检查3x3宫格
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                r, c = i + start_row, j + start_col
                if (r != row or c != col) and self.board[r][c] == num:
                    return False
        return True
    
    def is_solved(self):
        """检查数独是否已完成"""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def display(self):
        """显示数独板"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "=" * 45)
        print(f"  🎯 数独游戏 - 难度: {self.difficulty.upper()}")
        print("=" * 45)
        
        # 列号
        print("    ", end="")
        for i in range(1, self.size + 1):
            print(f"{i}  ", end="")
            if i % 3 == 0 and i < self.size:
                print(" ", end="")
        print()
        
        # 顶部边框
        print("  +" + "---+" * 9)
        
        for i in range(self.size):
            # 行号
            print(f"{i+1} |", end="")
            
            for j in range(self.size):
                # 数字显示
                if self.board[i][j] == 0:
                    value = " . "
                else:
                    value = f" {self.board[i][j]} "
                
                # 原始数字用蓝色显示，玩家输入用绿色
                if self.original_board[i][j] != 0:
                    print(f"\033[94m{value}\033[0m", end="")
                elif self.board[i][j] != 0:
                    print(f"\033[92m{value}\033[0m", end="")
                else:
                    print(value, end="")
                
                if (j + 1) % 3 == 0:
                    print("|", end="")
            
            print()
            
            # 分隔线
            if (i + 1) % 3 == 0:
                print("  +" + "---+" * 9)
            else:
                print("  +" + "   +" * 9)
        
        print("=" * 45)
        print("输入: 行 列 数字 (如: 3 5 7) | 0表示清除 | q 退出")
        print("=" * 45)
    
    def play(self):
        """主游戏循环"""
        while True:
            self.display()
            
            if self.is_solved():
                print("\n🏆 恭喜！你成功完成了数独！")
                break
            
            user_input = input("\n请输入: ").strip().lower()
            
            if user_input in ['q', 'quit', 'exit']:
                print("\n感谢游玩！")
                break
            
            try:
                parts = user_input.split()
                if len(parts) != 3:
                    print("❌ 格式错误！示例: 3 5 7")
                    input("按回车继续...")
                    continue
                
                row, col, num = map(int, parts)
                
                if not (1 <= row <= 9 and 1 <= col <= 9):
                    print("❌ 行列号必须在1-9之间！")
                    input("按回车继续...")
                    continue
                
                if not (0 <= num <= 9):
                    print("❌ 数字必须在0-9之间！")
                    input("按回车继续...")
                    continue
                
                row -= 1
                col -= 1
                
                # 检查是否是原始数字
                if self.original_board[row][col] != 0:
                    if num == 0:
                        print("❌ 不能清除原始数字！")
                        input("按回车继续...")
                        continue
                    elif num != self.original_board[row][col]:
                        print("❌ 不能修改原始数字！")
                        input("按回车继续...")
                        continue
                
                # 检查数字有效性
                if num != 0 and not self.is_valid(row, col, num):
                    print("❌ 该数字违反数独规则！")
                    input("按回车继续...")
                    continue
                
                # 更新棋盘
                self.board[row][col] = num
                
            except ValueError:
                print("❌ 请输入有效的数字！")
                input("按回车继续...")
                continue

def main():
    print("\n" + "=" * 50)
    print("🎯 欢迎来到数独小游戏！")
    print("=" * 50)
    
    # 选择难度
    print("\n选择难度等级:")
    print("1. 简单 (Easy) - 40个空格")
    print("2. 中等 (Medium) - 48个空格")
    print("3. 困难 (Hard) - 56个空格")
    
    while True:
        choice = input("\n请输入选项 (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            difficulties = { "1": "easy", "2": "medium", "3": "hard" }
            difficulty = difficulties[choice]
            break
        else:
            print("❌ 无效选项！请重新选择。")
    
    game = SudokuGame(difficulty)
    game.play()

if __name__ == "__main__":
    main()
