// src/app.test.js
describe('MainController', function() {
    let $controller, $httpBackend, $rootScope, $scope;

    beforeEach(module('myApp')); // Load the module

    beforeEach(inject(function(_$controller_, _$httpBackend_, _$rootScope_) {
        $controller = _$controller_;
        $httpBackend = _$httpBackend_;
        $rootScope = _$rootScope_;
        $scope = $rootScope.$new();
    }));

    afterEach(() => {
        // Ensure that all requests are flushed and no unexpected requests are made
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('should fetch monsters from the API on initialization', function() {
        // Mock the API response for the initialization request
        $httpBackend.expectGET('http://44.201.124.232:5000/monsters').respond(200, [
            { id: 1, name: 'Monster 1', description: 'First monster', type: 'Type A' },
            { id: 2, name: 'Monster 2', description: 'Second monster', type: 'Type B' }
        ]);

        // Create the controller, which will call fetchMonsters()
        const controller = $controller('MainController', { $scope });
        $httpBackend.flush(); // Simulate the response

        expect($scope.monsters.length).toBe(2);
        expect($scope.monsters[0].name).toBe('Monster 1');
    });

    it('should add a new monster', function() {
        const controller = $controller('MainController', { $scope });
        $scope.newMonster = { name: 'Monster 3', description: 'Third monster', type: 'Type C' };

        // Mock the API response for adding a monster
        $httpBackend.expectPOST('http://44.201.124.232:5000/monsters', $scope.newMonster).respond(201, {
            id: 3,
            name: 'Monster 3',
            description: 'Third monster',
            type: 'Type C'
        });

        $scope.addMonster();
        $httpBackend.flush(); // Simulate the response

        expect($scope.monsters.length).toBe(1);
        expect($scope.monsters[0].name).toBe('Monster 3');
    });

    it('should find a monster by ID', function() {
        const controller = $controller('MainController', { $scope });

        // Mock the API response for finding a monster
        $httpBackend.expectGET('http://44.201.124.232:5000/monsters/1').respond(200, {
            id: 1,
            name: 'Monster 1',
            description: 'First monster',
            type: 'Type A'
        });

        $scope.findMonsterById(1);
        $httpBackend.flush(); // Simulate the response

        expect($scope.foundMonster.name).toBe('Monster 1');
    });

    it('should delete a monster', function() {
        const controller = $controller('MainController', { $scope });
        $scope.monsters = [{ id: 1, name: 'Monster 1' }];

        // Mock the API response for deleting a monster
        $httpBackend.expectDELETE('http://44.201.124.232:5000/monsters/1').respond(200, {
            message: 'Monster deleted successfully!'
        });

        $scope.deleteMonster(1);
        $httpBackend.flush(); // Simulate the response

        expect($scope.monsters.length).toBe(0);
    });
});