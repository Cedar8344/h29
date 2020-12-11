#!/usr/local/cs/bin/python3
import os
import sys
import zlib

def main():
    #initialize arrays
    commits = []
    branches = []
    roots = []
    commitSorted = []

    #build branches/commits from git repo
    build_branches(branches)
    build_commits(commits)

    #topo sort + print
    topo_order_commits(commits, sorted(roots), commitSorted)
    print_topo_ordered_commits_with_branch_names(commits, commitSorted, branches)


# 5 Print
def print_topo_ordered_commits_with_branch_names(commits, commitSorted, branches):
    #print the wierd tree thing
    for i, c in enumerate(commitSorted): #for every c in sorted commits
        if i > 0 and commitSorted[i-1] not in commits[c].children:
            print('=', end='')
            print(*list(commits[c].children)) #print children of c

        if c in branches:
            print(c, end=' ')
            print(*sorted(branches[c]), sep=' ')
        else:
            print(c) #print actual

        if i+1 < len(commitSorted) and commitSorted[i+1] not in commits[c].parents:
            print(*list(commits[c].parents), sep=' ', end='')
            print('=\n')
    return 0

# 4 Sort Commit Graph
def topo_order_commits(commits, roots, commitSorted):
    #if commits found aren't a parent --> add to roots
    for i in commits:
        if not commits[i].parents:
            roots.append(i)
    v = set() #initialize visited array
    while roots: #iterate through roots
        n = commits[roots[-1]] #find node
        temp = False
        for c in n.children: #find children
            if c not in v: # if not visited
                roots.append(c)
                temp = True
                break
        if not temp: #if not added
            roots.pop()
            commitSorted.append(node.commit_hash)
            v.add(node.commit_hash) #undated visited array

# 3 Build Commit Graph
def build_commits(commits):
    p = os.path.realpath(os.path.join(get_git_dir(), "objects")) #objects path
    for root, _, files in os.walk(p):
        for i in files:
            pp = os.path.join(root, i)
            data = zlib.decompress(open(path, 'rb').read()) #use zlib lib
            if data.startswith('commit'): #if find a commit
                if pp.startswith(p): #if iterating path starts with p
                    pp = pp[len(p)+1:] #update array
                c = pp.replace('/', '').replace('\\', '') #remove special characters from path
                d = data.decode()
                parent = "" #initialize
                for line in d.split("\n"):
                    if line.startswith("parent "): #if node is a parent
                        parent = line[7:] #update parent
                if c not in commits: #in the commit isn't already added
                    commits[c] = CommitNode(c) #add another CommitNode
                if parent: #if its a parent node ...
                    if parent not in commits:
                        commits[parent] = CommitNode(parent)
                    commits[c].parents.add(parent)
                    commits[parent].children.add(c)

# 2 Find branch names from refs/heads
def find_branches(branches):
    p = os.path.join(os.path.join(find_git()),"refs"),"heads") #change to ref/heads folder
    b = [] #initialize branches array
    for root, _, files in os.walk(p):
        for i in files:
            pp = os.path.join(root, i)
            if path.startswith(p): #if iterating path starts with p
                pp = pp[len(p)+1:] #update array
            b.append(pp) #add found head/branch to temp
    for j in b:
        h = open(os.path.join(p, j), 'r').read().replace('\n', '')
        # if not already in branches, add b to branches
        if h not in branches:
            branches[h] = []
        branches[h].append(b)


# 1 Discover .git directory
def find_git()
    p = os.path.abspath(os.curdir) # search current dir
    while os.path.dirname(p) != p: #if dirname(path) = path, at root, stop searching
        # search directory
        for i in os.listdir(p):
            if(i == ".git"): #found git, return
                return os.path.realpath(os.path.join(p, i))
        #iterate down
        p = os.path.join(p, os.pardir)
    #if while fails to return, p = root, return failure
    sys.exit("no git directory found")

# CommitNode class
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()


if __name__ == '__main__':
    main()

