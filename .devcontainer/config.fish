# Fish functions
## Setting "!!" to input the last command
function bind_bang
    switch (commandline -t)
        case "!"
            commandline -t -- $history[1]
            commandline -f repaint
        case "*"
            commandline -i !
    end
end
bind ! bind_bang

# Setting the prompt visuals - Inspired by eromatiya/fishblocks
## Left-hand prompt
function fish_prompt
	echo (_block_pwd)(set_color red)'>'(set_color yellow)'>'(set_color green)'> '(set_color -b normal)' '
end

## Right-hand prompt
function fish_right_prompt
	echo -ne (_block_status)(_block_git)(_block_time_stamp)(set_color normal)
end

## PWD block
function _block_pwd
	set block (set_color -b black -o green)' '(prompt_pwd)' '
	echo $block
end

## Time stamp block
function _block_time_stamp
	set block (set_color -b brcyan -o black)' '(date +%H:%M:%S)' '
	echo $block
end

## Status block
function _block_status
	set -l last_status $status
	if not test $status -eq 0
		set block (set_color -b red yellow)" $last_status "
	else
		set block (set_color -b black green)" $last_status "
	end
	echo $block
end

## Getting the Git status to change the color of the block
function _fishblocks_git_status
	if [ (not git diff --no-ext-diff --quiet --exit-code 2>/dev/null && echo 0) ]
		set git_bg red
	else
		set git_bg green
	end
	echo $git_bg
end

## Git block
function _block_git
	if [ (fish_git_prompt) ]
		set git_bg (_fishblocks_git_status)
		set block (fish_git_prompt)'  '
	else
		set git_bg normal
		set block (fish_git_prompt)
	end
	echo (set_color -b $git_bg -o black) $block
end


# Removing the welcome greeting
set fish_greeting


# Setting up aliases
alias vim="nvim"
alias ll="eza -lha --tree --level=3"
alias cat="bat"
alias grep="rg"


# Setting up zoxide - database path gets replaced with the PWD of when startup.sh is run 
set -x _ZO_DATA_DIR "zoxideDatabasePath/.devcontainer"
zoxide init --cmd cd fish | source

# Terminal Ricing
fastfetch
