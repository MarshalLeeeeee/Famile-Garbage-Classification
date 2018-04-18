//
//  main.cpp
//  dispatch_algorithm
//
//  Created by 赵通 on 2018/4/14.
//  Copyright © 2018年 赵通. All rights reserved.
//

#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <queue>
using namespace std;

struct node{
    int x;
    int y;
    node():x(0),y(0){}
    node(int xx,int yy):x(xx),y(yy){
        
    }
};
struct car{
    string car_id;
    string nearest;
    node coor;
    int space;
    car():space(0),car_id(""){}
    car(string id,int xx,int yy,int s):car_id(id),coor(xx,yy),space(s),nearest(""){
        
    }
};
struct collector{
    string collector_id;
    string nearest;
    node coor;
    int space;
    collector():space(0){}
    collector(string id,int xx,int yy,int s):collector_id(id),coor(xx,yy),space(s),nearest(""){
        
    }
};
struct transaction{
    int type;
    vector<car>::iterator itr;
    node new_coor;
    int new_space;
    string new_car_id;
};
vector <car> car_vector;
vector <collector> collector_vector;
vector<node> dump_station_vector;
queue<transaction> transaction_queue;

double distance(node x1,node x2)
{
    return sqrt((x1.x-x2.x)*(x1.x-x2.x)+(x1.y-x2.y)*(x1.y-x2.y));
}

int threshold = 100;//when one car 's space is larger than 100 than the car must go to the nearst dump_station.

int main(int argc, const char * argv[]) {
    char ch;
    car temp_car;
    collector temp_collector;
    node temp_node;
    transaction temp_transaction;
    cout<<"please entry all messages one by one, end with '@' ,garbage_car using 'g',collector using 'c',dump_stations using 'd':"<<'\n';
    while (1)
    {
        cin>>ch;
        /*switch (ch) {
            case '@':
                
                break;
                
            default:
                break;
        }*/
        if(ch=='@')
        {
            break;
        }
        if(ch=='g')
        {
            cin>>temp_car.car_id>>temp_car.coor.x>>temp_car.coor.y>>temp_car.space;
            temp_car.nearest="";
            car_vector.push_back(temp_car);
        }
        if(ch=='c')
        {
        cin>>temp_collector.collector_id>>temp_collector.coor.x>>temp_collector.coor.y>>temp_collector.space;
            temp_collector.nearest="";
            collector_vector.push_back(temp_collector);
        }
        if(ch=='d')
        {
            cin>>temp_node.x>>temp_node.y;
            dump_station_vector.push_back(temp_node);
        }
    }
    double dis = 0;
    double min_dis = INT_MAX;
    //int index = -1;
    bool find = 0;
    while (!collector_vector.empty())
    {
        while (!transaction_queue.empty())
        {
            auto i = transaction_queue.front();
            transaction_queue.pop();
            if(i.type==0)
            {
                i.itr->coor = i.new_coor;
                i.itr->space = i.new_space;
            }
            else if(i.type==1)
            {
                temp_car.car_id = i.new_car_id;
                temp_car.space = 0;
                temp_car.nearest = "";
                temp_car.coor = i.new_coor;
                
                car_vector.push_back(temp_car);
            }
        }
        int t =1;
        for(auto i=car_vector.begin();i!=car_vector.end();)
        {
            min_dis = INT_MAX;
            if(i->space>threshold)//we need to delete this car and put the car into tranction
            {
                for (auto j:dump_station_vector)
                {
                    dis=distance(i->coor,j);
                    if(dis<min_dis)
                    {
                        min_dis = dis;
                        temp_transaction.new_car_id = i->car_id;
                        temp_transaction.new_space = 0;
                        temp_transaction.new_coor=j;
                        temp_transaction.type = 1;
                    }
                }
                cout<<i->car_id<<" will go to coordinate "<<temp_transaction.new_coor.x<<' '<<temp_transaction.new_coor.y<<" to throw garbage!"<<'\n';
                transaction_queue.push(temp_transaction);
                i=car_vector.erase(i);
            }
            else
            {
                //do nothing
                ++i;
            }
        }
        int tt = 1;
        for (auto i=car_vector.begin();i!=car_vector.end();i++)
        {
            min_dis = INT_MAX;
            for (auto j = collector_vector.begin();j!=collector_vector.end();j++)
            {
                dis = distance(i->coor,j->coor);
                if(dis<min_dis)
                {
                    min_dis = dis;
                    i->nearest = j->collector_id;
                }
            }
        }
        for (auto i=collector_vector.begin();i!=collector_vector.end();)
        {
            min_dis = INT_MAX;
            find = 0;
            auto index = car_vector.end();
            for(auto j=car_vector.begin();j!=car_vector.end();j++)
            {
                dis = distance(i->coor, j->coor);
                if (dis<min_dis) {
                    min_dis = dis;
                    i->nearest = j->car_id;
                    index = j;
                    find=1;
                }
            }
            if(find&&i->nearest==index->car_id&&index->nearest==i->collector_id)
            {
                cout<<index->car_id<<" will get the "<<i->coor.x<<' '<<i->coor.y<<" 's garbage"<<'\n';
                temp_transaction.type =0;
                temp_transaction.itr = index;
                temp_transaction.new_coor = i->coor;
                temp_transaction.new_space = index->space+i->space;
                transaction_queue.push(temp_transaction);
                i=collector_vector.erase(i);
            }
            else
            {
                i++;
            }
        }
    }
    return 0;
}
