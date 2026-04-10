import sys
import re

with open('index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# 1) Add flags state
old_state = '''                answers: new Array(100).fill(null), // Lưu index đáp án người dùng chọn
                timeStart: null,'''
new_state = '''                answers: new Array(100).fill(null), // Lưu index đáp án người dùng chọn
                flags: new Array(100).fill(false), // Flag trạng thái phân vân
                timeStart: null,'''
res = orig.replace(old_state, new_state)

# 2) Let's add the flag rendering logic in renderQuestion()
old_render_q = '''                // Cập nhật Header
                document.getElementById('q-counter').innerText = `${idx + 1} / ${total}`;
                document.getElementById('q-category').innerText = `Hạng mục: ${catName}`;
                document.getElementById('q-progress').style.width = `${((idx + 1) / total) * 100}%`;'''
new_render_q = '''                // Cập nhật Header
                document.getElementById('q-counter-desktop').innerText = `${idx + 1} / ${total}`;
                document.getElementById('q-counter-mobile').innerText = `${idx + 1} / ${total}`;
                document.getElementById('q-counter-mobile-toggle').innerText = `${idx + 1} / ${total}`;
                document.getElementById('q-category').innerText = `${catName}`;
                document.getElementById('q-progress').style.width = `${((idx + 1) / total) * 100}%`;

                // Flag Badge & Button
                const isFlagged = this.state.flags[idx];
                const badge = document.getElementById('q-flag-badge');
                if(isFlagged) {
                    badge.classList.remove('hidden');
                    document.getElementById('btn-flag').classList.add('bg-yellow-50', 'dark:bg-yellow-500/10');
                    document.getElementById('btn-flag-text').innerText = 'Bỏ Phân vân';
                } else {
                    badge.classList.add('hidden');
                    document.getElementById('btn-flag').classList.remove('bg-yellow-50', 'dark:bg-yellow-500/10');
                    document.getElementById('btn-flag-text').innerText = 'Đánh dấu Phân vân';
                }
                
                // RENDER GRID
                this.renderGrid();
'''
res = res.replace(old_render_q, new_render_q)

# 3) Update selectAnswer to trigger grid render
old_sel_ans = '''            selectAnswer(optIndex) {
                this.state.answers[this.state.currentQuestion] = optIndex;
            },'''
new_sel_ans = '''            selectAnswer(optIndex) {
                this.state.answers[this.state.currentQuestion] = optIndex;
                this.renderGrid(); // Update grid state to "Đã làm"
            },
            
            toggleFlag() {
                const idx = this.state.currentQuestion;
                this.state.flags[idx] = !this.state.flags[idx];
                this.renderQuestion(); // Re-render to show/hide badge
            },

            jumpToQuestion(idx) {
                this.state.currentQuestion = idx;
                this.renderQuestion();
            },

            toggleGridMobile() {
                const content = document.getElementById('grid-content');
                const icon = document.getElementById('icon-toggle-grid');
                if (content.style.maxHeight && content.style.maxHeight !== '0px') {
                    content.style.maxHeight = '0px';
                    content.style.opacity = '0';
                    icon.style.transform = 'rotate(0deg)';
                } else {
                    content.style.maxHeight = '1000px';
                    content.style.opacity = '1';
                    icon.style.transform = 'rotate(180deg)';
                }
            },

            renderGrid() {
                const grid = document.getElementById('q-nav-grid');
                if (!grid) return;
                
                grid.innerHTML = '';
                for (let i = 0; i < this.data.questions.length; i++) {
                    const btn = document.createElement('button');
                    
                    btn.className = `w-full aspect-square rounded-md sm:rounded-lg font-tech font-bold text-[10px] sm:text-xs xl:text-sm flex items-center justify-center transition-all duration-200 border relative hover:scale-105 `;
                    
                    const isAnswered = this.state.answers[i] !== null;
                    const isCurrent = i === this.state.currentQuestion;
                    const isFlagged = this.state.flags[i];
                    
                    if (isCurrent) {
                        btn.className += `bg-neon-blue text-white border-neon-blue shadow-[0_0_8px_rgba(0,243,255,0.6)] z-10 `;
                    } else if (isAnswered) {
                        btn.className += `bg-green-500/10 dark:bg-green-500/20 text-green-600 dark:text-green-400 border-green-500/50 hover:bg-green-500/20 `;
                    } else {
                        btn.className += `bg-gray-50 dark:bg-gray-800/80 text-gray-500 dark:text-gray-400 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 `;
                    }
                    
                    if (isFlagged) {
                        const dot = document.createElement('div');
                        dot.className = `absolute right-0 top-0 w-2 h-2 sm:w-2.5 sm:h-2.5 rounded-full bg-yellow-400 shadow-[0_0_5px_rgba(250,204,21,1)] transform translate-x-1/3 -translate-y-1/3 z-20`;
                        btn.appendChild(dot);
                        
                        if (!isCurrent && !isAnswered) {
                            btn.className += `border-yellow-400/50 `;
                        }
                    }
                    
                    btn.innerHTML += (i + 1);
                    btn.onclick = () => {
                        this.jumpToQuestion(i);
                        if(window.innerWidth < 1280) {
                            this.toggleGridMobile(); // auto close on mobile
                        }
                    };
                    
                    grid.appendChild(btn);
                }
            },'''
res = res.replace(old_sel_ans, new_sel_ans)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(res)
print("Javascript replaced")
