// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TaskManager {
    // Roles: 0 = None, 1 = Read, 2 = Write, 3 = Admin
    enum Role { None, Read, Write, Admin }

    struct Task {
        uint id;
        string title;
        string description;
        bool completed;
        uint timestamp;
    }

    struct TaskList {
        uint id;
        string name;
        string description;
        address owner;
        uint timestamp;
        uint taskCount;
        mapping(uint => Task) tasks;
        mapping(address => Role) roles;
    }

    uint public listCount;
    mapping(uint => TaskList) private lists;

    event ListCreated(uint indexed listId, address indexed owner, string name);
    event TaskAdded(uint indexed listId, uint taskId, string title);
    event RoleAssigned(uint indexed listId, address indexed user, Role role);
    event RoleRemoved(uint indexed listId, address indexed user);
    event TaskCompleted(uint indexed listId, uint taskId);

    modifier onlyOwner(uint _listId) {
        require(lists[_listId].owner == msg.sender, "Not list owner");
        _;
    }

    modifier onlyAuthorized(uint _listId, Role requiredRole) {
        TaskList storage list = lists[_listId];
        Role userRole = list.roles[msg.sender];
        require(userRole >= requiredRole || list.owner == msg.sender, "Not authorized");
        _;
    }

    function createList(string memory _name, string memory _description) public returns (uint) {
        listCount++;
        TaskList storage list = lists[listCount];
        list.id = listCount;
        list.name = _name;
        list.description = _description;
        list.owner = msg.sender;
        list.timestamp = block.timestamp;
        list.taskCount = 0;
        list.roles[msg.sender] = Role.Admin;  // Owner is admin
        emit ListCreated(listCount, msg.sender, _name);
        return listCount;
    }

    function addTask(uint _listId, string memory _title, string memory _description) public onlyAuthorized(_listId, Role.Write) returns (uint) {
        TaskList storage list = lists[_listId];
        list.taskCount++;
        list.tasks[list.taskCount] = Task(list.taskCount, _title, _description, false, block.timestamp);
        emit TaskAdded(_listId, list.taskCount, _title);
        return list.taskCount;
    }

    function completeTask(uint _listId, uint _taskId) public onlyAuthorized(_listId, Role.Write) {
        TaskList storage list = lists[_listId];
        require(_taskId > 0 && _taskId <= list.taskCount, "Invalid taskId");
        list.tasks[_taskId].completed = true;
        emit TaskCompleted(_listId, _taskId);
    }

    function assignRole(uint _listId, address _user, Role _role) public onlyOwner(_listId) {
        TaskList storage list = lists[_listId];
        list.roles[_user] = _role;
        emit RoleAssigned(_listId, _user, _role);
    }

    function removeRole(uint _listId, address _user) public onlyOwner(_listId) {
        TaskList storage list = lists[_listId];
        list.roles[_user] = Role.None;
        emit RoleRemoved(_listId, _user);
    }

    // For reading data off-chain, you can implement getter functions if needed.
}
