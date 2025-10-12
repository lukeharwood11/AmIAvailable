import React, { useEffect, useState } from 'react';
import { useReduxAiUsage } from '../../../hooks/useReduxAiUsage';
import { Note, Card, Text, Button } from '../../../components';
import { AiUsageData } from '../../../redux/types/ai-usage.types';
import { MdRefresh, MdInfo, MdCalendarMonth } from 'react-icons/md';
import styles from './AiUsageTab.module.css';

const AiUsageTab: React.FC = () => {
    const {
        records,
        totalCount,
        pagination,
        loading,
        error,
        hasRecords,
        currentPage,
        totalPages,
        loadAiUsageCost,
        loadAiUsageByDateRange,
    } = useReduxAiUsage();

    const [isRefreshing, setIsRefreshing] = useState(false);
    const [selectedMonth, setSelectedMonth] = useState(() => {
        const now = new Date();
        return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    });
    const [monthlyCost, setMonthlyCost] = useState<number>(0);
    const [monthlyCostLoading, setMonthlyCostLoading] = useState(false);

    // Load initial data for current month
    useEffect(() => {
        const parts = selectedMonth.split('-');
        const year = parseInt(parts[0] || '', 10);
        const month = parseInt(parts[1] || '', 10);
        
        if (!isNaN(year) && !isNaN(month)) {
            const startDate = new Date(year, month - 1, 1);
            const endDate = new Date(year, month, 0); // Last day of the month
            
            loadAiUsageByDateRange({ 
                skip: 0, 
                take: 10, 
                startDate: startDate.toISOString(), 
                endDate: endDate.toISOString() 
            });
            loadMonthlyCost(startDate.toISOString(), endDate.toISOString());
        }
    }, [selectedMonth, loadAiUsageByDateRange]);

    const loadMonthlyCost = async (startDate: string, endDate: string) => {
        setMonthlyCostLoading(true);
        try {
            const result = await loadAiUsageCost({ startDate, endDate });
            const costData = result.payload;
            if (costData && typeof costData === 'object' && 'cost' in costData) {
                setMonthlyCost(costData.cost as number);
            } else {
                setMonthlyCost(0);
            }
        } catch (error) {
            console.error('Failed to load monthly cost:', error);
            setMonthlyCost(0);
        } finally {
            setMonthlyCostLoading(false);
        }
    };

    const handleRefresh = async () => {
        setIsRefreshing(true);
        try {
            const parts = selectedMonth.split('-');
            const year = parseInt(parts[0] || '', 10);
            const month = parseInt(parts[1] || '', 10);
            
            if (!isNaN(year) && !isNaN(month)) {
                const startDate = new Date(year, month - 1, 1);
                const endDate = new Date(year, month, 0);
                
                await loadAiUsageByDateRange({ 
                    skip: 0, 
                    take: 10, 
                    startDate: startDate.toISOString(), 
                    endDate: endDate.toISOString() 
                });
                await loadMonthlyCost(startDate.toISOString(), endDate.toISOString());
            }
        } finally {
            setIsRefreshing(false);
        }
    };

    const handleMonthChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedMonth(event.target.value);
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            const parts = selectedMonth.split('-');
            const year = parseInt(parts[0] || '', 10);
            const month = parseInt(parts[1] || '', 10);
            
            if (!isNaN(year) && !isNaN(month)) {
                const startDate = new Date(year, month - 1, 1);
                const endDate = new Date(year, month, 0);
                const newSkip = Math.max(0, pagination.skip - pagination.take);
                
                loadAiUsageByDateRange({ 
                    skip: newSkip, 
                    take: pagination.take, 
                    startDate: startDate.toISOString(), 
                    endDate: endDate.toISOString() 
                });
            }
        }
    };

    const handleNextPage = () => {
        if (currentPage < totalPages) {
            const parts = selectedMonth.split('-');
            const year = parseInt(parts[0] || '', 10);
            const month = parseInt(parts[1] || '', 10);
            
            if (!isNaN(year) && !isNaN(month)) {
                const startDate = new Date(year, month - 1, 1);
                const endDate = new Date(year, month, 0);
                const newSkip = pagination.skip + pagination.take;
                
                loadAiUsageByDateRange({ 
                    skip: newSkip, 
                    take: pagination.take,
                    startDate: startDate.toISOString(), 
                    endDate: endDate.toISOString() 
                });
            }
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const formatCost = (cost: number) => {
        return `$${cost.toFixed(4)}`;
    };

    const getModelName = (record: AiUsageData) => {
        return record.metadata?.model || record.usage?.model || 'Unknown Model';
    };

    const renderUsageRecord = (record: AiUsageData) => (
        <div key={record.id} className={styles.usageRecord}>
            <div className={styles.recordHeader}>
                <div className={styles.recordInfo}>
                    <Text variant="body" color="grey-800" weight="medium">
                        {getModelName(record)}
                    </Text>
                    <Text variant="body-small" color="grey-600">
                        {formatDate(record.created_at)}
                    </Text>
                </div>
                <div className={styles.recordCost}>
                    <Text variant="body" color="grey-800" weight="medium">
                        {formatCost(record.cost)}
                    </Text>
                </div>
            </div>
            
            <div className={styles.recordDetails}>
                {record.usage.prompt_tokens && (
                    <div className={styles.detailItem}>
                        <Text variant="body-small" color="grey-600">
                            Prompt Tokens: {record.usage.prompt_tokens.toLocaleString()}
                        </Text>
                    </div>
                )}
                {record.usage.completion_tokens && (
                    <div className={styles.detailItem}>
                        <Text variant="body-small" color="grey-600">
                            Completion Tokens: {record.usage.completion_tokens.toLocaleString()}
                        </Text>
                    </div>
                )}
                {record.usage.total_tokens && (
                    <div className={styles.detailItem}>
                        <Text variant="body-small" color="grey-600">
                            Total Tokens: {record.usage.total_tokens.toLocaleString()}
                        </Text>
                    </div>
                )}
            </div>
        </div>
    );

    return (
        <div className={styles.aiUsageTab}>
            {/* Summary Card */}
            <Card variant="default" padding="large" className={styles.summaryCard}>
                <div>
                    <div className={styles.summaryHeader}>
                        <Text variant="heading-small" color="grey-800">
                            AI Usage Summary
                        </Text>
                        <Button
                            variant="secondary"
                            size="small"
                            onClick={handleRefresh}
                            disabled={loading || isRefreshing}
                            leftIcon={<MdRefresh size={16} />}
                        >
                            {isRefreshing ? 'Refreshing...' : 'Refresh'}
                        </Button>
                    </div>
                    <Note leftIcon={<MdInfo size={16} />} variant='info'>
                        AI pricing data is privileged data, this will be removed in future releases.
                    </Note>
                </div>
                
                <div className={styles.monthSelector}>
                    <div className={styles.monthInput}>
                        <MdCalendarMonth size={20} className={styles.calendarIcon} />
                        <input
                            type="month"
                            value={selectedMonth}
                            onChange={handleMonthChange}
                            className={styles.monthInputField}
                        />
                    </div>
                </div>
                
                <div className={styles.summaryStats}>
                    <div className={styles.statItem}>
                        <Text variant="body-small" color="grey-600">
                            Monthly Cost
                        </Text>
                        <Text variant="heading-small" color="grey-800">
                            {monthlyCostLoading && !monthlyCost ? '$-.----' : formatCost(monthlyCost)}
                        </Text>
                    </div>
                    <div className={styles.statItem}>
                        <Text variant="body-small" color="grey-600">
                            Current Page
                        </Text>
                        <Text variant="heading-small" color="grey-800">
                            {currentPage} of {totalPages}
                        </Text>
                    </div>
                </div>
            </Card>

            {/* Usage Records */}
            <Card variant="default" padding="large" className={styles.recordsCard}>
                <div className={styles.recordsHeader}>
                    <Text variant="heading-small" color="grey-800">
                        Usage Records
                    </Text>
                    {hasRecords && (
                        <Text variant="body-small" color="grey-600">
                            Showing {pagination.skip + 1}-{Math.min(pagination.skip + pagination.take, totalCount)} of {totalCount}
                        </Text>
                    )}
                </div>

                {loading && !hasRecords ? (
                    <div className={styles.loadingState}>
                        <Text variant="body" color="grey-600">
                            Loading usage records...
                        </Text>
                    </div>
                ) : error ? (
                    <div className={styles.errorState}>
                        <Text variant="body" color="danger">
                            Error: {error}
                        </Text>
                        <Button
                            variant="primary"
                            size="small"
                            onClick={handleRefresh}
                            className={styles.retryButton}
                        >
                            Try Again
                        </Button>
                    </div>
                ) : !hasRecords ? (
                    <div className={styles.emptyState}>
                        <MdInfo size={48} className={styles.emptyIcon} />
                        <Text variant="body" color="grey-600">
                            No AI usage records found.
                        </Text>
                        <Text variant="body-small" color="grey-500">
                            Your AI usage will appear here once you start using Amia.
                        </Text>
                    </div>
                ) : (
                    <>
                        <div className={styles.recordsList}>
                            {records.map(renderUsageRecord)}
                        </div>

                        {/* Pagination Controls */}
                        <div className={styles.pagination}>
                            <div className={styles.paginationInfo}>
                                <Text variant="body-small" color="grey-600">
                                    Page {currentPage} of {totalPages}
                                </Text>
                            </div>
                            
                            <div className={styles.paginationControls}>
                                <Button
                                    variant="secondary"
                                    size="small"
                                    onClick={handlePreviousPage}
                                    disabled={currentPage <= 1 || loading}
                                >
                                    Previous
                                </Button>
                                
                                <Button
                                    variant="secondary"
                                    size="small"
                                    onClick={handleNextPage}
                                    disabled={currentPage >= totalPages || loading}
                                >
                                    Next
                                </Button>
                            </div>
                        </div>
                    </>
                )}
            </Card>
        </div>
    );
};

export default AiUsageTab;