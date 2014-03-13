angular.module("BongApp.Index", [
    "BongApp.Common",
]).controller('IndexController', function($rootScope, $scope, $state, $http){
    $rootScope.isAuthenticated();


});
