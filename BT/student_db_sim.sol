// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StudentDB {

    struct Student {
        string name;
        uint256 rollno;
        uint256 age;
        string batch;
    }

    Student[] public students;
    address public admin;

    mapping(uint256 => bool) private _exists;
    mapping(uint256 => uint256) private rollToIndex;

    event addStudentEvent(string name, uint256 indexed rollno);
    event updateStudentEvent(string name, uint256 indexed rollno);
    event removeStudentEvent(uint256 indexed rollno);

    modifier byAdmin() {
        require(msg.sender == admin, "Access Denied!");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    function addStudent(
        string calldata _name,
        uint256 _rollno,
        uint256 _age,
        string calldata _batch
    ) external byAdmin {
        require(bytes(_name).length > 0, "Name cannot be empty!");
        require(_rollno > 0, "Enter valid roll no!");
        require(_age > 0 && _age < 20, "Enter valid age!");
        require(!_exists[_rollno], "Entry for this roll no already exists!");

        Student memory enteredStudent = Student({
            name: _name,
            rollno: _rollno,
            age: _age,
            batch: _batch
        });

        students.push(enteredStudent);
        uint256 idx = students.length - 1;
        _exists[_rollno] = true;
        rollToIndex[_rollno] = idx;

        emit addStudentEvent(_name, _rollno);
    }

    function updateStudent(
        uint256 _rollno,
        string calldata _name,
        uint256 _age,
        string calldata _batch
    ) external byAdmin {
        require(_exists[_rollno], "Student does not exist");
        require(bytes(_name).length > 0, "Name cannot be empty!");
        require(_age > 0 && _age < 20, "Enter valid age!");

        uint256 idx = rollToIndex[_rollno];
        Student storage s = students[idx];
        s.name = _name;
        s.age = _age;
        s.batch = _batch;

        emit updateStudentEvent(_name, _rollno);
    }

    function removeStudent(uint256 _rollno) external byAdmin {
        require(_exists[_rollno], "Student does not exist");

        uint256 idx = rollToIndex[_rollno];
        uint256 lastIndex = students.length - 1;

        if (idx != lastIndex) {
            Student storage lastStudent = students[lastIndex];
            students[idx] = lastStudent;
            rollToIndex[lastStudent.rollno] = idx;
        }

        students.pop();
        delete rollToIndex[_rollno];
        delete _exists[_rollno];

        emit removeStudentEvent(_rollno);
    }

    function getStudentByRoll(uint256 _rollno) public view returns (string memory, uint256, uint256, string memory) {
        require(_exists[_rollno], "Student does not exist");
        uint256 idx = rollToIndex[_rollno];
        Student storage fetchedStudent = students[idx];
        return (fetchedStudent.name, fetchedStudent.rollno, fetchedStudent.age, fetchedStudent.batch);
    }

    function getStudent(uint256 idx) public view returns (string memory, uint256, uint256, string memory) {
        require(idx < students.length, "Index out of bound!");
        Student storage fetchedStudent = students[idx];
        return (fetchedStudent.name, fetchedStudent.rollno, fetchedStudent.age, fetchedStudent.batch);
    }

    function getStudentsCount() public view returns (uint256) {
        return students.length;
    }
}
