angular.module("BongApp.Common", [
]).directive('navbar', function(localStorageService, $rootScope, $state) {
    return {
        restrict: 'E',
        templateUrl: "{{ angular_template('navbar.html') }}",
        link: function (scope, element, attrs) {
            scope.logout = function(){
                localStorageService.clearAll();
                $rootScope.bongAuthToken = null;
                $state.go('login');
            };
        }
    }
})
