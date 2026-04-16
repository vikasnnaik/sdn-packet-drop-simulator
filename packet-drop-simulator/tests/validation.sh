#!/bin/bash

# Validation script for Packet Drop Simulator
# Run after starting controller and topology

echo "======================================"
echo "Packet Drop Simulator - Validation Suite"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

test_case() {
    local name=$1
    local command=$2
    local expected=$3
    
    echo -n "Testing: $name ... "
    result=$(eval "$command" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}PASSED${NC}"
        ((PASSED++))
    else
        echo -e "${RED}FAILED${NC}"
        echo "  Expected: $expected"
        echo "  Got: ${result:0:100}"
        ((FAILED++))
    fi
}

echo -e "\n${YELLOW}1. Basic Connectivity Tests${NC}"
echo "--------------------------------------"

# Test 1: Ping from h1 to h2 without drop rules
test_case "Ping h1->h2 (no drop)" \
    "sudo mn -c 2>/dev/null; sudo h1 ping -c 2 10.0.0.2 2>&1" \
    "0% packet loss"

# Test 2: Verify Mininet is installed
test_case "Mininet installed" \
    "which mn" \
    "/usr/bin/mn"

# Test 3: Verify Ryu is installed
test_case "Ryu installed" \
    "which ryu-manager" \
    "/usr/bin/ryu-manager"

echo -e "\n${YELLOW}2. Controller Tests${NC}"
echo "--------------------------------------"

# Test 4: Controller file exists
test_case "Controller file exists" \
    "ls controller/drop_controller.py" \
    "drop_controller.py"

# Test 5: Topology file exists
test_case "Topology file exists" \
    "ls topology/custom_topology.py" \
    "custom_topology.py"

echo -e "\n${YELLOW}3. Packet Drop Specific Tests${NC}"
echo "--------------------------------------"

# Test 6: Drop rule configuration
test_case "Drop rules configured" \
    "grep -c 'drop_rules.append' controller/drop_controller.py" \
    "3"

# Test 7: Packet logging
test_case "Packet logging implemented" \
    "grep '_log_dropped_packet' controller/drop_controller.py" \
    "_log_dropped_packet"

echo -e "\n======================================"
echo -e "RESULTS: ${GREEN}$PASSED PASSED${NC} / ${RED}$FAILED FAILED${NC}"
echo "======================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All validation tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Please check your setup.${NC}"
    exit 1
fi
