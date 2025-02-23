var app = angular.module('myApp', [])
app.controller('MainController', function($scope, $http) {
    $scope.newMonster = {};
    $scope.monsters = [];
    $scope.foundMonster = null; // Initialize found monster

    // Fetch all monsters on controller initialization
    $scope.fetchMonsters = function() {
        $http.get('http://44.201.124.232:5000/monsters')  // Update to your Flask API endpoint
            .then(function(response) {
                $scope.monsters = response.data; // Store the fetched monsters
                console.log("Fetched monsters:", $scope.monsters); // Debug log
            })
            .catch(function(error) {
                console.error("Error fetching monsters:", error); // Log any errors
            });
    };

    // Call fetchMonsters when the controller is initialized
    $scope.fetchMonsters();

    // Add a new monster
    $scope.addMonster = function() {
        $http.post('http://44.201.124.232:5000/monsters', $scope.newMonster)  // Update to your Flask API endpoint
            .then(function(response) {
                $scope.monsters.push(response.data);
                $scope.newMonster = {};
            });
    };

    // Delete a monster
    $scope.deleteMonster = function(id) {
        $http.delete('http://44.201.124.232:5000/monsters/' + id)  // Corrected URL
            .then(function() {
                $scope.monsters = $scope.monsters.filter(monster => monster.id !== id);
                if ($scope.foundMonster && $scope.foundMonster.id === id) {
                    $scope.foundMonster = null; // Clear found monster if deleted
                }
            });
    };

    $scope.findMonsterById = function(id) {
        // Fetch the monster by ID
        $http.get('http://44.201.124.232:5000/monsters/' + id)  // Corrected URL
            .then(function(response) {
                $scope.foundMonster = response.data; // Store the found monster
                console.log("Found Monster:", id); // Debug log
            })
            .catch(function(error) {
                alert('Monster not found!');
                $scope.foundMonster = null; // Clear found monster if not found
            });
    };
});