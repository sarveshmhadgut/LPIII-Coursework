// SPDX-License-Identifier: MIT

pragma solidity ^ 0.8.0;

contract BankAccount {
    address public owner;
    uint256 private balance;


    event Withdrawal(address indexed account, uint256 amount);
    event Deposit(address indexed account, uint256 amount);

    constructor ()  {
        owner = msg.sender;
        balance = 0;
    }

    modifier byOwner() {
        require(owner == msg.sender, "Action restricted!");
        _;
    }

    function deposit() public payable{
        require(msg.value > 0, "Invalid deposit amount!");
        balance += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) public byOwner {
        require(amount > 0, "Invalid withdrawl amount!");
        require(amount <= balance, "Insufficient funds!");

        balance -= amount;
        payable(owner).transfer(amount);
        emit Withdrawal(msg.sender, amount);

    }

    function getBalance() public view returns(uint256) {
        return balance;
    }
}
