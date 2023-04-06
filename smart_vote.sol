// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract VotingSystem {

    // Voter structure
    struct Voter {
        uint voterId;
        bool isRegistered;
        bool hasVoted;
        uint votedCandidateId;
    }

    // Candidate structure
    struct Candidate {
        uint candidateId;
        string name;
        uint voteCount;
    }

    // State variables
    address public owner;
    bool public votingOpen;
    mapping(address => Voter) public voters;
    Candidate[] public candidates;

    // Events
    event VoterRegistered(address voter);
    event VotingStarted();
    event VotingStopped();
    event Voted(address voter, uint candidateId);
    event CandidateAdded(string name);

    // Constructor
    constructor() {
        owner = msg.sender;
        votingOpen = false;
    }

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    // Register a new voter
    function registerVoter(uint _voterId) public {
        require(!voters[msg.sender].isRegistered, "You are already registered");
        voters[msg.sender] = Voter(_voterId, true, false, 0);
        emit VoterRegistered(msg.sender);
    }

    // Add a new candidate
    function addCandidate(string memory _name) public onlyOwner {
        candidates.push(Candidate(candidates.length, _name, 0));
        emit CandidateAdded(_name);
    }

    // Start the voting
    function startVoting() public onlyOwner {
        require(!votingOpen, "Voting is already open");
        votingOpen = true;
        emit VotingStarted();
    }

    // Stop the voting
    function stopVoting() public onlyOwner {
        require(votingOpen, "Voting is not open");
        votingOpen = false;
        emit VotingStopped();
    }

    // Vote for a candidate
    function vote(uint _candidateId) public {
        require(voters[msg.sender].isRegistered, "You are not registered");
        require(votingOpen, "Voting is not open");
        require(!voters[msg.sender].hasVoted, "You have already voted");
        voters[msg.sender].hasVoted = true;
        voters[msg.sender].votedCandidateId = _candidateId;
        candidates[_candidateId].voteCount += 1;
        emit Voted(msg.sender, _candidateId);
}
// Get the candidate list
function getCandidates() public view returns (Candidate[] memory) {
    return candidates;
}

// Get the total number of votes for a candidate
function getVoteCount(uint _candidateId) public view returns (uint) {
    return candidates[_candidateId].voteCount;
}

// Check if a voter has already voted
function hasVoted() public view returns (bool) {
    return voters[msg.sender].hasVoted;
}

// Check if the voting is open
function isVotingOpen() public view returns (bool) {
    return votingOpen;
}
}