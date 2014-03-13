angular.module("BongApp.Auth", [
    "BongApp.Common",
]).controller('LoginController', function($rootScope, $scope, $state, $http, localStorageService){
    if ((typeof $rootScope.bongAuthToken === 'string') && ($rootScope.bongAuthToken.length > 0)) {
        $rootScope.bongAuthToken = localStorageService.get("token");
        $state.go('index');
        return;
    }
    $scope.authenticate = function(){
        $rootScope.bongAuthToken = $scope.token;
        localStorageService.add("token", $scope.token);
        $state.go('index');
    };
});
