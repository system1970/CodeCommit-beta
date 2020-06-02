# https://codeforces.com/problemset/problem/791/A
# Bear and Big Brother

a,b = list(map(int,input().split()))
ans = 0
while a&lt;=b:
    a*=3
    b*=2
    ans+=1
print(ans)